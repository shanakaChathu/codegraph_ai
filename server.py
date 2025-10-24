from fastapi import FastAPI
from pydantic import BaseModel
from agents.parser_graph import parse_repo, build_graph, query_graph
from pydantic import BaseModel
from agents.agent import run_codegraph_agent
import json
import os
from config import CFG
from langchain_openai import ChatOpenAI
from agents.tools import load_repo, search_graph_tool, read_code, write_code, create_pr
from langchain.agents import create_agent

app = FastAPI(title="CodeGraph.AI")

class Ping(BaseModel):
    msg: str

@app.post("/ping")
def ping(p: Ping):
    return {"ok": True, "echo": p.msg}

@app.get("/graph-demo")
def graph_demo(repo_path: str, q: str = ""):
    summary = parse_repo(repo_path)
    G = build_graph(summary)
    hits = query_graph(G, q, topk=8)
    return {"functions": len(summary), "nodes": G.number_of_nodes(), "hits": hits[:8]}


class RunReq(BaseModel):
    repo_path: str
    branch_name: str
    jira_id: str


@app.post("/run-agent")
def run(req: RunReq):
    return {"ok": True, "data": run_codegraph_agent(req.repo_path,req.branch_name,req.jira_id )}



