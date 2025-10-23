import ast
from pathlib import Path
import networkx as nx

def parse_repo(repo_path):
    items = []
    for py in Path(repo_path).rglob("*.py"):
        try:
            text = py.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=str(py))
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                calls = []
                for n in ast.walk(node):
                    if isinstance(n, ast.Call) and hasattr(n.func, "id"):
                        calls.append(n.func.id)
                items.append({
                    "file": str(py),
                    "func": node.name,
                    "doc": ast.get_docstring(node) or "",
                    "calls": calls
                })
    return items

def build_graph(repo_summary):
    G = nx.DiGraph()
    idx = {}
    for it in repo_summary:
        key = f"{it['file']}::{it['func']}"
        G.add_node(key, file=it["file"], func=it["func"], doc=it["doc"])
        idx.setdefault(it["func"], []).append(key)
    for it in repo_summary:
        caller = f"{it['file']}::{it['func']}"
        for callee_name in it["calls"]:
            for callee in idx.get(callee_name, []):
                G.add_edge(caller, callee)
    return G

def query_graph(G, text, topk=8):
    q = (text or "").lower()
    hits = [n for n, d in G.nodes(data=True)
            if q in n.lower() or q in (d.get("doc","").lower())]
    expanded = set()
    for n in hits[:topk]:
        expanded.add(n)
        expanded.update(list(G.successors(n)))
        expanded.update(list(G.predecessors(n)))
    return list(expanded)[:topk]
