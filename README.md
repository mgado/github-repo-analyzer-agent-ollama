# 🤖 GitHub Repo Analyzer Agent

This project is a web-based tool that uses a local Large Language Model (LLM) to act as an AI expert, providing a high-level analysis of any public GitHub repository.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mgado/github-repo-analyzer-agent-ollama/blob/main/GitHub%20Repo%20Analyzer%20agent.ipynb)

## ✨ Features

-   **Expert Analysis:** Get a structured summary of any GitHub repo's purpose, technology stack, and potential use cases.
-   **Flexible Model Selection:** Choose from a curated list of top open-source LLMs or enter the name of any other model available on Ollama.
-   **Dual Interface:** Run the application with a user-friendly Gradio web UI or directly from the command line.
-   **Automatic Setup:** The application can automatically download any required Ollama models on the first run.

## 🛠️ Setup and Installation

### Prerequisites

-   Python 3.9+
-   [Ollama](https://ollama.com/) installed and running on your local machine.

### Installation Steps

1.  **Download and Install Ollama:**
    -   **Windows:** Download and run the installer from the [Ollama website](https://ollama.com/).
    -   **macOS & Linux:** Run the following command in your terminal:
        ```bash
        curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
        ```

2.  **Clone the Project Repository:**
    ```bash
    git clone <repo-url>
    cd githubRepoAnalyzerAgent
    ```

3.  **Install Dependencies and Download Model:**
    -   **For macOS & Linux:**
        Run the provided setup script. It will install Python packages and pull a default LLM.
        ```bash
        chmod +x setup.sh
        ./setup.sh
        ```
    -   **For Windows (Manual Setup):**
        Run the following commands in your Command Prompt or PowerShell:
        ```cmd
        :: Install the required Python packages
        pip install -r requirements.txt

        :: Pull a default LLM from Ollama
        ollama pull llama3:8b

## 🚀 How to Run

### Web Interface (UI)

To launch the Gradio web application, run:
```bash
python app_core.py
```

Then, open the local URL printed in your terminal (e.g., http://127.0.0.1:7860) in your web browser.

### Command-Line Interface (CLI)
You can also run the analysis directly from your terminal.
```bash
python app_core.py --url <GITHUB_REPO_URL> [--model <MODEL_NAME>]
```
Example: 
```bash
python app_core.py --url https://github.com/huggingface/transformers --model gpt-oss:20b
```

## 📁 Project Structure
- app_core.py: Main application file (UI and CLI logic).
- config.py: Stores the curated list of models.
- github_utils.py: Fetches README content from GitHub.
- llm_analyzer.py: Handles the interaction with the LLM.
- ollama_utils.py: Manages Ollama models.
- requirements.txt: Lists the required Python packages.
- setup.sh: Automates the installation process (only for macOS and Linux).
- test_app.py: Contains simple tests for the core functions.
