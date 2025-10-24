import os
from dotenv import load_dotenv
load_dotenv()

class CFG:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    JIRA_SERVER = os.getenv("JIRA_SERVER")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER")
    GITHUB_REPO = os.getenv("GITHUB_REPO")

    GIT_AUTHOR_NAME = os.getenv("GIT_AUTHOR_NAME", "CodeGraph.AI")
    GIT_AUTHOR_EMAIL = os.getenv("GIT_AUTHOR_EMAIL", "bot@codegraph.ai")

    PULL_REQ_BRANCH= "develop"