import ollama
from typing import List

# This module handles all direct interactions with the Ollama service.

def get_local_models() -> List[str]:
    """Gets the list of models already pulled locally."""
    try:
        models_info = ollama.list()
        return [model['model'] for model in models_info['models']]
    except Exception:
        return []

def ensure_model_is_pulled(model_name: str):
    """Checks if a model is available locally, and pulls it if not."""
    local_models = get_local_models()
    if model_name not in local_models:
        try:  
            print(f"Model '{model_name}' not found locally. Pulling from Ollama...")
            ollama.pull(model_name)
            print("Model pulled successfully.")
        except Exception as e:  
            # Raise a standard error that the main app function will catch and display.
            raise RuntimeError(f"Failed to pull model '{model_name}'. Please check the model name and your connection. Details: {e}")
    
    
