import json
import os
from config import CFG
from langchain_openai import ChatOpenAI
from agents.tools import load_repo, search_graph_tool, read_code, write_code, create_pr
from langchain.agents import create_agent

def run_codegraph_agent(story_text: str, repo_path: str,branch_name:str) -> dict:
    # Set the API key in environment for LangChain to pick up
    os.environ['OPENAI_API_KEY'] = CFG.OPENAI_API_KEY
    
    # Use the older, more stable initialization method
    llm = ChatOpenAI(
        api_key=CFG.OPENAI_API_KEY,
        model="gpt-4o-mini",  # can also use 'gpt-4o' or 'gpt-4-turbo'
        temperature=0.1,
    )

    tools = [load_repo, search_graph_tool, read_code, write_code, create_pr]

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
6) create_pr with branch {branch_name} and title equal to the Story title
Return JSON with keys: pr_url, target_file.
"""

    agent = create_agent(tools=tools,model=llm,system_prompt=prompt,)
    result = agent.invoke({"story": story_text, "repo": repo_path, "branch_name":branch_name},config={"recursion_limit": 50})
    
    try:
        return json.loads(result)
    except Exception:
        return {"raw": result}

# def run_codegraph_agent(story_text: str, repo_path: str) -> dict:
#     # Initialize OpenAI client directly
#     client = OpenAI(api_key=CFG.OPENAI_API_KEY)
    
#     # Initialize tools
#     tools = {
#         "load_repo": load_repo,
#         "search_graph_tool": search_graph_tool,
#         "read_code": read_code,
#         "write_code": write_code,
#         "create_pr": create_pr
#     }
    
#     # System prompt
#     system_prompt = """You are CodeGraph.AI, an AI agent that helps implement code changes based on user stories.

# You have access to the following tools:
# - load_repo(repo_path): Load a repository and build its code graph
# - search_graph_tool(query): Search the code graph for relevant functions
# - read_code(path): Read the contents of a file
# - write_code(path, content): Write content to a file
# - create_pr(branch_name, title): Create a pull request

# You must follow these steps:
# 1. Load the repository using load_repo
# 2. Search for relevant functions using search_graph_tool
# 3. Choose a target file and read its contents
# 4. Make minimal changes to implement the story
# 5. Write the updated file
# 6. Create a pull request

# Always return your final result as JSON with keys: pr_url, target_file."""

#     # Initial user prompt
#     user_prompt = f"""
# Story: {story_text}
# Repo: {repo_path}

# Please implement this story by following the required steps.
# """

#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_prompt}
#     ]

#     # Run the agent loop
#     max_iterations = 10
#     for iteration in range(max_iterations):
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages,
#             temperature=0.1,
#         )
        
#         assistant_message = response.choices[0].message.content
#         messages.append({"role": "assistant", "content": assistant_message})
        
#         # Check if the response contains tool calls
#         if "load_repo(" in assistant_message or "search_graph_tool(" in assistant_message or "read_code(" in assistant_message or "write_code(" in assistant_message or "create_pr(" in assistant_message:
#             # Extract and execute tool calls
#             tool_results = execute_tool_calls(assistant_message, tools, repo_path)
            
#             if tool_results:
#                 messages.append({"role": "user", "content": f"Tool results: {tool_results}"})
#             else:
#                 break
#         else:
#             # Check if we have a final JSON result
#             try:
#                 # Try to extract JSON from the response
#                 json_match = re.search(r'\{[^}]*"pr_url"[^}]*\}', assistant_message)
#                 if json_match:
#                     return json.loads(json_match.group())
#                 else:
#                     return {"raw": assistant_message}
#             except:
#                 return {"raw": assistant_message}
    
#     return {"raw": "Agent completed maximum iterations"}

# def execute_tool_calls(message: str, tools: dict, repo_path: str) -> str:
#     """Execute tool calls found in the message"""
#     results = []
    
#     # Look for tool calls in the message
#     if "load_repo(" in message:
#         try:
#             result = tools["load_repo"](repo_path)
#             results.append(f"load_repo result: {result}")
#         except Exception as e:
#             results.append(f"load_repo error: {str(e)}")
    
#     if "search_graph_tool(" in message:
#         # Extract query from the call
#         import re
#         match = re.search(r'search_graph_tool\("([^"]*)"\)', message)
#         if match:
#             query = match.group(1)
#             try:
#                 result = tools["search_graph_tool"](query)
#                 results.append(f"search_graph_tool result: {result}")
#             except Exception as e:
#                 results.append(f"search_graph_tool error: {str(e)}")
    
#     if "read_code(" in message:
#         # Extract path from the call
#         import re
#         match = re.search(r'read_code\("([^"]*)"\)', message)
#         if match:
#             path = match.group(1)
#             try:
#                 result = tools["read_code"](path)
#                 results.append(f"read_code result: {result[:500]}...")  # Truncate for readability
#             except Exception as e:
#                 results.append(f"read_code error: {str(e)}")
    
#     if "write_code(" in message:
#         # Extract path and content from the call
#         import re
#         match = re.search(r'write_code\("([^"]*)",\s*"([^"]*)"\)', message, re.DOTALL)
#         if match:
#             path = match.group(1)
#             content = match.group(2)
#             try:
#                 result = tools["write_code"](path, content)
#                 results.append(f"write_code result: {result}")
#             except Exception as e:
#                 results.append(f"write_code error: {str(e)}")
    
#     if "create_pr(" in message:
#         # Extract branch and title from the call
#         import re
#         match = re.search(r'create_pr\("([^"]*)",\s*"([^"]*)"\)', message)
#         if match:
#             branch = match.group(1)
#             title = match.group(2)
#             try:
#                 result = tools["create_pr"](branch, title)
#                 results.append(f"create_pr result: {result}")
#             except Exception as e:
#                 results.append(f"create_pr error: {str(e)}")
    
#     return "\n".join(results) if results else ""
