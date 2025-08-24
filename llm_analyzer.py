#This module contains the core logic for interacting with the LLM to perform the analysis.
import ollama
import time
from typing import Tuple

def analyze_repo_with_llm(context: str, model_name: str) -> Tuple[str, str]:
    """Uses a local LLM via Ollama to analyze the repo content."""
    
    prompt = f"""
    You are an expert senior AI researcher with 20 years of experience.
    Your task is to analyze the following GitHub repository's README file and provide a structured, concise, and insightful summary.

    **README Content:**
    ---
    {context}
    ---

    **Your Analysis:**
    Provide the output in the following markdown format:

    ### 🚀 Project Summary
    (A brief, one-paragraph summary of the project's main goal and functionality.)

    ### 🛠️ Key Technologies & Libraries
    (A bulleted list of the primary technologies, languages, and libraries mentioned or implied.)

    ### 💡 Potential Use Cases
    (A bulleted list of 2-3 potential real-world applications for this project.)

    ### 📈 Complexity
    (Your expert opinion on the project's complexity: Beginner, Intermediate, or Advanced.)
    """
    
    try:
        print("-> Sending request to LLM...")
        start_time = time.time() # Start the timer
        response = ollama.chat(
            model= model_name,  # Or 'gemma2', 'llamma3', 'gemma3:1B', 'gemma3:270M'
            messages=[{'role': 'user', 'content': prompt}]
        )
        end_time = time.time() # End the timer
        print("-> Received response from LLM.")
        duration = end_time - start_time
        llm_response = response['message']['content']
        # Append the timing information to the response for display
        timing_info = f"*LLM processing time: {duration:.2f} seconds.*"
        
        print("-> [*] "+timing_info[1:-1])
        return llm_response, timing_info

    except Exception as e:
        print(f"Error communicating with LLM: {e})")
        return f"Error <repoAnalyzerAgent> communicating with LLM {model_name}: {e}", ""