from pathlib import Path
from git import Repo, Actor
from github import Github
from langchain.tools import tool
from config import CFG
from agents.parser_graph import parse_repo, build_graph, query_graph

STATE = {
    "repo_path": None,
    "graph": None,
    "target_file": None,
    "jira_story": None,  # will use in Step 4
}

@tool("load_repo")
def load_repo(repo_path: str) -> str:
    """Load a repository and build its code graph for analysis."""
    summary = parse_repo(repo_path)
    G = build_graph(summary)
    STATE["repo_path"] = repo_path
    STATE["graph"] = G
    return f"Loaded repo with {len(summary)} functions and {G.number_of_edges()} edges."

@tool("search_graph")
def search_graph_tool(query: str) -> str:
    """Search the code graph for relevant functions based on a query."""
    G = STATE.get("graph")
    if not G: return "Graph not ready."
    hits = query_graph(G, query, topk=8)
    return "\n".join(hits)

@tool("read_code")
def read_code(path: str) -> str:
    """Read the contents of a file from the filesystem."""
    return Path(path).read_text(encoding="utf-8")

@tool("write_code")
def write_code(path: str, content: str) -> str:
    """Write content to a file on the filesystem."""
    Path(path).write_text(content, encoding="utf-8")
    STATE["target_file"] = path
    return f"UPDATED {path}"

@tool("create_pr")
def create_pr(branch_name: str, title: str) -> str:
    """Create a new branch, commit changes, and create a pull request on GitHub."""
    repo_dir = STATE["repo_path"]
    if not repo_dir: return "ERROR: repo_path missing."

    repo = Repo(repo_dir)
    # branch
    if branch_name in [h.name for h in repo.heads]:
        branch = repo.heads[branch_name]
    else:
        branch = repo.create_head(branch_name)
    branch.checkout()

    # stage changes (only changed file or all)
    if STATE.get("target_file"):
        repo.git.add(STATE["target_file"])
    else:
        repo.git.add(A=True)

    author = Actor(CFG.GIT_AUTHOR_NAME, CFG.GIT_AUTHOR_EMAIL)
    repo.index.commit(title, author=author, committer=author)

    # push
    origin = repo.remote(name="origin")
    origin.push(refspec=f"{branch_name}:{branch_name}")

    # PR
    gh = Github(CFG.GITHUB_TOKEN)
    g_repo = gh.get_repo(f"{CFG.GITHUB_OWNER}/{CFG.GITHUB_REPO}")
    pr = g_repo.create_pull(
        title=f"[CodeGraph.AI] {title}",
        body="Automated change by CodeGraph.AI",
        head=branch_name,
        base="main"   # change to 'develop' if needed
    )
    return pr.html_url
