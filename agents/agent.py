import json
import os
from config import CFG
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from agents.tools import load_repo, search_graph_tool, read_code, write_code, create_pr

def run_codegraph_agent(story_text: str, repo_path: str) -> dict:
    # Set the API key in environment for LangChain to pick up
    os.environ['OPENAI_API_KEY'] = CFG.OPENAI_API_KEY
    
    # Use the older, more stable initialization method
    llm = ChatOpenAI(
        model_name="gpt-4o-mini", 
        temperature=0.1,
        openai_api_key=CFG.OPENAI_API_KEY
    )
    tools = [load_repo, search_graph_tool, read_code, write_code, create_pr]
    agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    prompt = f"""
You are CodeGraph.AI.
Story: {story_text}
Repo: {repo_path}

Steps you MUST follow:
1) load_repo("{repo_path}")
2) use search_graph_tool with keywords from the Story to find candidate "file::func" nodes
3) choose one target file (everything before '::' is the path)
4) read_code on that file
5) make minimal changes to implement the Story; return FULL updated file to write_code
6) create_pr with branch "fix/demo" and title equal to the Story title
Return JSON with keys: pr_url, target_file.
"""
    result = agent.run(prompt)
    try:
        return json.loads(result)
    except Exception:
        return {"raw": result}
