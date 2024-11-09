from openai import OpenAI
import logging
import sys
import traceback
from pathlib import Path
from typing import Dict, Any

# Add root directory to Python path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from config import OLLAMA_CONFIG, LOG_CONFIG

# Configure logging
logging.basicConfig(level=LOG_CONFIG["level"], format=LOG_CONFIG["format"])
logger = logging.getLogger(__name__)

def debug_function(error_info: Dict[str, Any], context: str = None) -> Dict[str, str]:
    """
    Analyze errors and suggest fixes using LLM.
    
    Args:
        error_info (Dict[str, Any]): Dictionary containing error details
            {
                'error_type': str,
                'error_message': str,
                'traceback': str,
                'code_snippet': str (optional),
                'variables': dict (optional)
            }
        context (str, optional): Additional context about the error
        
    Returns:
        Dict[str, str]: Analysis and suggestions
            {
                'analysis': str,
                'root_cause': str,
                'fix': str,
                'prevention': str
            }
    """
    try:
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        
        logger.info(f"Processing debug analysis for {error_info['error_type']}")
        
        # Format error information more clearly
        error_context = f"""
ERROR DETAILS:
Type: {error_info['error_type']}
Message: {error_info['error_message']}

TRACEBACK:
{error_info['traceback']}
"""
        
        if 'code_snippet' in error_info:
            error_context += f"\nCODE:\n{error_info['code_snippet']}"
            
        if 'variables' in error_info:
            error_context += "\nVARIABLE STATE:\n"
            for var, value in error_info['variables'].items():
                error_context += f"{var} = {value}\n"
                
        if context:
            error_context += f"\nCONTEXT:\n{context}"

        completion = client.chat.completions.create(
            model=OLLAMA_CONFIG["model"],
            messages=[
                {
                    "role": "system", 
                    "content": """You are an expert debugging assistant. Analyze errors and provide clear, actionable solutions.
                    ONLY respond in this exact format with these exact sections:
                    
                    ANALYSIS:
                    <single line brief error analysis>
                    
                    ROOT_CAUSE:
                    <single line root cause>
                    
                    FIX:
                    <code or steps to fix>
                    
                    PREVENTION:
                    <bullet points for prevention>
                    
                    DO NOT include any other text or sections."""
                },
                {
                    "role": "user",
                    "content": f"Debug this error:\n{error_context}"
                }
            ],
            temperature=0.1
        )
        
        response = completion.choices[0].message.content.strip()
        
        # Parse response sections with improved handling
        sections = {
            'analysis': '',
            'root_cause': '',
            'fix': '',
            'prevention': ''
        }
        
        current_section = None
        current_content = []
        
        for line in response.split('\n'):
            line = line.strip()
            if line in ['ANALYSIS:', 'ROOT_CAUSE:', 'FIX:', 'PREVENTION:']:
                if current_section:
                    sections[current_section.lower().rstrip(':')] = '\n'.join(current_content).strip()
                current_section = line.lower().rstrip(':')
                current_content = []
            elif line:  # Only append non-empty lines
                current_content.append(line)
                
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Validate all sections are present
        for section in sections:
            if not sections[section]:
                sections[section] = "No information provided"
        
        logger.info("Debug analysis completed")
        return sections
        
    except Exception as e:
        logger.error(f"Error in debug analysis: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Test with a common error
        test_error = {
            'error_type': 'IndexError',
            'error_message': 'list index out of range',
            'traceback': """Traceback (most recent call last):
  File "test.py", line 5, in <module>
    print(numbers[5])
IndexError: list index out of range""",
            'code_snippet': """numbers = [1, 2, 3]
print(numbers[5])""",
            'variables': {
                'numbers': '[1, 2, 3]',
                'len(numbers)': '3'
            }
        }
        
        result = debug_function(test_error, "This happens when processing user input")
        
        print("\nDebug Analysis:")
        for section, content in result.items():
            print(f"\n{section.upper()}:")
            print(content)
            
    except Exception as e:
        logger.error(f"Failed to process: {str(e)}") 