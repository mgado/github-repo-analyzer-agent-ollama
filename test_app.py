# simple tests to verify that the core functions of the application are working as expected
import pytest
from unittest.mock import patch, MagicMock
from github_utils import get_readme_content
from llm_analyzer import analyze_repo_with_llm

# A valid, public GitHub repository URL for testing
VALID_URL = "https://github.com/openai/gpt-oss"
INVALID_URL = "https://github.com/this/repo-does-not-exist"

def test_get_readme_content_success():
    """Tests that README content can be successfully fetched from a valid URL."""
    content = get_readme_content(VALID_URL)
    assert "Error<repoAnalyzerAgent>" not in content
    assert "openai" in content

def test_get_readme_content_failure():
    """Tests that an error is returned for an invalid URL."""
    content = get_readme_content(INVALID_URL)
    assert "Error<repoAnalyzerAgent>" in content


@patch('llm_analyzer.ollama.chat')
def test_analyze_repo_with_llm_success(mock_ollama_chat):
    """
    Tests the LLM analysis function with mock data.
    Tests the main analysis function with a mocked Ollama API call.
    Note: This test assumes Ollama is running and has a model available.
    For a true unit test, you would mock the ollama.chat call.
    """
    mock_readme = "This is a test README for a project using Python, Ollama and Gradio."
    # Using a small, fast model
    model = "gemma3:270M" 
    
    
    mock_response = {
    'message': {
        'content': '### 🚀 Project Summary\nThis is a mocked summary.'
    }
    }
    mock_ollama_chat.return_value = mock_response
    
    analysis, timing_info = analyze_repo_with_llm(mock_readme, model)
    
    assert "Error" not in analysis
    assert "Project Summary" in analysis
    assert "seconds" in timing_info
    

@patch('llm_analyzer.ollama.chat')
def test_analyze_repo_with_llm_invalid_model(mock_ollama_chat):
    """
    Tests that the analysis function returns a user-friendly error
    when a non-existent model name is provided.
    """
    # Simulate the error that the ollama library would raise
    
    mock_ollama_chat.side_effect = Exception("Model 'invalid-model' not found")
    
    mock_readme = "This is a test README."
    invalid_model = "this-model-does-not-exist-12345"
    
    analysis, timing = analyze_repo_with_llm(mock_readme, invalid_model)
    
    # Check that a clear error message is returned to the user
    assert "Error" in analysis
    assert invalid_model in analysis # The error should mention the invalid model name
    

@pytest.mark.optional    
def test_analyze_repo_with_llm_with_real_ollama_server_running():
    """
    Tests the LLM analysis function with mock data.
    Note: This test assumes Ollama is running and has a model available.
    For a true unit test, you would mock the ollama.chat call.
    """
    mock_readme = "This is a test README for a project using Python, Ollama and Gradio."
    # Using a small, fast model
    model = "gemma3:270M" 
    
    analysis, timing_info = analyze_repo_with_llm(mock_readme, model)
    
    assert "Error" not in analysis
    assert "Project Summary" in analysis
    assert "seconds" in timing_info


@pytest.mark.optional
def test_analyze_repo_with_llm_invalid_model_with_real_ollama_server_running():
    """
    Tests that the analysis function returns a user-friendly error
    when a non-existent model name is provided.
    """
    mock_readme = "This is a test README."
    invalid_model = "this-model-does-not-exist-12345"
    
    analysis, timing = analyze_repo_with_llm(mock_readme, invalid_model)
    
    # Check that a clear error message is returned to the user
    assert "Error" in analysis
    assert invalid_model in analysis # The error should mention the invalid model name
