# This module is responsible for fetching content from GitHub.
import requests

def get_readme_content(github_url: str) -> str:
    """Fetches and cleans the README content from a GitHub repo URL."""
    try:
        # To get the raw README, we can adjust the URL
        # e.g., https://github.com/user/repo -> https://raw.githubusercontent.com/user/repo/main/README.md
        if "github.com" not in github_url:
            return "Error<repoAnalyzerAgent>: Please provide a valid GitHub URL."
            
        parts = github_url.strip("/").split("/")
        user = parts[-2]
        repo = parts[-1]
        
        # Try common main branch names
        for branch in ["main", "master","develop", "dev"]:
            raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/README.md"
            response = requests.get(raw_url)
            if response.status_code == 200:
                return response.text
        
        return "Error<repoAnalyzerAgent>: Could not find README.md in 'main' or 'master' branch."

    except Exception as e:
        return f"Error<repoAnalyzerAgent> fetching content: {e}"


