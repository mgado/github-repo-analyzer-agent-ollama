# simple tests to verify that the core functions of the application are working as expected
import pytest
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

def test_analyze_repo_with_llm():
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
    

def test_analyze_repo_with_llm_invalid_model():
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
