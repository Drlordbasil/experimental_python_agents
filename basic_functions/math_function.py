from openai import OpenAI
import logging
import sys
from pathlib import Path

# Add root directory to Python path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from config import OLLAMA_CONFIG, LOG_CONFIG

# Configure logging
logging.basicConfig(level=LOG_CONFIG["level"], format=LOG_CONFIG["format"])
logger = logging.getLogger(__name__)

def math_function(question: str) -> str:
    """
    Process mathematical questions using LLM.
    
    Args:
        question (str): Mathematical question to process
        
    Returns:
        str: Calculated result
        
    Raises:
        Exception: If API call fails
    """
    try:
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        
        logger.info(f"Processing math question: {question}")
        
        completion = client.chat.completions.create(
            model=OLLAMA_CONFIG["model"],
            messages=[
                {
                    "role": "system", 
                    "content": """You are a mathematical computation function. You ONLY output the numerical result.
                    Examples:
                    Input: 2 + 2=
                    Output: 4
                    
                    Input: What is 5 * 3?
                    Output: 15
                    
                    Input: Calculate 10/2
                    Output: 5"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=OLLAMA_CONFIG["temperature"]
        )
        
        response = completion.choices[0].message.content.strip()
        logger.info(f"Received response: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing math question: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        result = math_function("2 + 2=")
        print(f"Result: {result}")
    except Exception as e:
        logger.error(f"Failed to process: {str(e)}")
