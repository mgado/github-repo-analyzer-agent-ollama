# This is the main entry point of the application. Imports other modules, defines the UI, and orchestrate the logic.
import gradio as gr
from typing import Tuple
import argparse

# Import functions from our other modules
from config import CURATED_MODEL_LIST
from ollama_utils import ensure_model_is_pulled
from github_utils import get_readme_content
from llm_analyzer import analyze_repo_with_llm



def analyze_github_repo(url: str, model_name: str, progress = gr.Progress(track_tqdm=True)) -> Tuple[str, str]:
    """The main function that ties everything together for the UI."""
    if not url or not model_name:
        return "Please enter a GitHub repository URL to begin and select a model.", "Please enter a GitHub repository URL to begin and select a model."

    # step 0: start 
    msg_0 = "Initiating github repo anlysis..."
    if isinstance(progress, gr.Progress):
        progress(0, desc=msg_0)
    else:
        print(msg_0)


    # Step 1: Ensure the model is available
    msg_1 = f"Step (1/4) Checking model: {model_name}..."
    try:
        if isinstance(progress, gr.Progress):
            progress(0.25, desc=msg_1)
        else:
            print(msg_1)
        ensure_model_is_pulled(model_name)
    except (gr.Error, RuntimeError) as e:
        return str(e), str(e)

    # Step 2: Fetch README content
    msg_2 = f"Step (2/4) Fetching content for: {url}..."
    if isinstance(progress, gr.Progress):
        progress(0.5, desc=msg_2)
    else:
        print(msg_2)
    readme_content = get_readme_content(url)
    if "Error<repoAnalyzerAgent>" in readme_content:
        return readme_content, readme_content

    # Step 3: Analyze with the LLM
    msg_3 = f"Step (3/4) Analyzing content with LLM -> {model_name}..."
    if isinstance(progress, gr.Progress):
        progress(0.75, desc=msg_3)
    else:
        print(msg_3)
    analysis, timing_info = analyze_repo_with_llm(readme_content, model_name)
    #print(timing_info)

    # Step 4: Done
    msg_4 = "Step (4/4) Done!"
    if isinstance(progress, gr.Progress):
        progress(1, desc= msg_4)
    else:
        print(msg_4)
    return analysis, timing_info


def clear_fields():
    """Returns empty values to clear all input and output fields."""
    # Clears: url_input, analysis_output, time_output, model_dropdown
    return "", "", "", CURATED_MODEL_LIST[0]

def create_ui():
    """Creates the layout and returns the Gradio UI Blocks"""
    with gr.Blocks() as iface:
        gr.Markdown("# 🤖 GitHub Repo Analyzer Agent")
        gr.Markdown("Enter a GitHub repo URL to get an expert analysis from a local LLM. The first analysis with a model may take some time as the model loads into memory.")

        with gr.Row():
            with gr.Column(scale=3):
                url_input = gr.Textbox(
                    lines=15,
                    placeholder="e.g., https://github.com/ollama/ollama",
                    label="GitHub Repository URL"
                )
            with gr.Column(scale=1):
                model_dropdown = gr.Dropdown(
                    choices=CURATED_MODEL_LIST, 
                    value=CURATED_MODEL_LIST[0], 
                    label="Select or Enter a LLM Model Name",
                    allow_custom_value=True
                )
                submit_btn = gr.Button("Submit", variant="primary")
                stop_btn = gr.Button("Stop", variant="stop")
                clear_btn = gr.Button("Clear")
                time_output = gr.Textbox(label="Processing information", elem_id="time-output")

        with gr.Row():
            analysis_output = gr.Markdown(label="Expert Analysis", elem_id="analysis-output")

        gr.Examples(
            examples=[
                ["https://github.com/openai/gpt-oss"],
                ["https://github.com/facebookresearch/llama"],
                ["https://github.com/huggingface/transformers"],
                ["https://github.com/matlab-deep-learning/llms-with-matlab"],
            ],
            inputs=url_input
        )

        # Event handling
        analysis_event = submit_btn.click(
            fn=analyze_github_repo,
            inputs=[url_input, model_dropdown],
            outputs=[analysis_output, time_output]
        )
        stop_btn.click(fn=None, inputs=None, outputs=None, cancels=[analysis_event])
        clear_btn.click(fn=clear_fields, inputs=None, outputs=[url_input, analysis_output, time_output, model_dropdown])
    
    return iface


def main_cli():
    """Handles the command-line interface logic."""
    parser = argparse.ArgumentParser(description="GitHub Repo Analyzer CLI")
    parser.add_argument("--url", required=True, type=str, help="URL of the GitHub repository to analyze.")
    parser.add_argument("--model", type=str, default=CURATED_MODEL_LIST[0], help=f"Name of the Ollama model to use (default: {CURATED_MODEL_LIST[0]}).")
    args = parser.parse_args()

    print("--- GitHub Repo Analyzer CLI ---")
    analysis, timing_info = analyze_github_repo(args.url, args.model, progress=None)
    print("\n--- Analysis Result ---")
    print(analysis)
    print("-----------------------")
    print(f"Processing Time: {timing_info}")
    print("-----------------------")
    
    

if __name__ == "__main__":
    import sys
    # Check if any command-line arguments for the CLI were provided
    if len(sys.argv) > 1 and any(arg.startswith('--') for arg in sys.argv):
        main_cli()
    else:
        # If no CLI arguments, launch the Gradio UI
        app_ui = create_ui()
        print("Launching Gradio Interface...")
        app_ui.launch(debug=True)
