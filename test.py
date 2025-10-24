import json
import os

from gitdb.typ import str_tag_type
from config import CFG
from langchain_openai import ChatOpenAI
from agents.tools import load_repo, search_graph_tool, read_code, write_code, create_pr,get_jira_story

from langchain.agents import create_agent

def run_codegraph_agent(repo_path: str,branch_name:str,jira_id:str) -> dict:
    # Set the API key in environment for LangChain to pick up
    os.environ['OPENAI_API_KEY'] = CFG.OPENAI_API_KEY
    
    # Use the older, more stable initialization method
    llm = ChatOpenAI(
        api_key=CFG.OPENAI_API_KEY,
        model="gpt-4o-mini",  # can also use 'gpt-4o' or 'gpt-4-turbo'
        temperature=0.1,
    )

    tools = [get_jira_story,load_repo, search_graph_tool, read_code, write_code, create_pr]

    prompt = f"""
You are CodeGraph.AI.
Repo: {repo_path}

Steps you MUST follow:
1) Use get_jira_story to fetch Jira story {jira_id}.
2) load_repo("{repo_path}")
3) use search_graph_tool with keywords from the Story to find candidate "file::func" nodes
4) choose one target file (everything before '::' is the path)
5) read_code on that file
6) make minimal changes to implement the Story; return FULL updated file to write_code
7) Create a branch 'fix/{branch_name}/{jira_id}' and open PR using create_pr.
Return JSON with keys: pr_url, target_file.
"""
    agent = create_agent(tools=tools,model=llm,system_prompt=prompt,)
    result = agent.invoke({"repo": repo_path, "branch_name":branch_name,"jira_id":jira_id},config={"recursion_limit": 50})
    
    try:
        return json.loads(result)
    except Exception:
        return {"raw": result}


if __name__ == "__main__":
    #story_text = "currently in the get_stoptime function things are hadr coded in the re.seach function. i want change this function to move those string to constant file and refer from there"
    #story_text = "there is function in this code to get the airlne logo. currently its .png but not its changed to the .jpg. can you do the required changes in the repo"
    repo_path = "C:\\Users\\shana\\OneDrive\\Desktop\\AI_Olympiad\\amadeus-flight-booking-django"
    branch_name="feat/jira_integration"
    jira_id="CA-1"
    result = run_codegraph_agent(repo_path,branch_name,jira_id)
    print(result)


