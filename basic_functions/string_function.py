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

def string_function(operation: str, text: str) -> str:
    """
    Process string operations using LLM.
    
    Args:
        operation (str): Operation to perform (e.g., 'reverse', 'capitalize', 'count_words')
        text (str): Text to process
        
    Returns:
        str: Processed result
        
    Raises:
        Exception: If API call fails
    """
    try:
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        
        logger.info(f"Processing string operation: {operation} on text: {text[:50]}...")
        
        completion = client.chat.completions.create(
            model=OLLAMA_CONFIG["model"],
            messages=[
                {
                    "role": "system", 
                    "content": """You are a string manipulation function. You ONLY output the exact result with NO additional text.
                    Examples:
                    Input Operation: reverse
                    Input Text: hello world
                    Output: dlrow olleh
                    
                    Input Operation: capitalize
                    Input Text: hello world
                    Output: HELLO WORLD
                    
                    Input Operation: count_words
                    Input Text: hello beautiful world
                    Output: 3
                    
                    Input Operation: remove_punctuation
                    Input Text: Hello, World! How are you?
                    Output: Hello World How are you
                    
                    IMPORTANT: 
                    - Return ONLY the processed result
                    - For remove_punctuation, preserve spaces between words
                    - For count_words, return only the number
                    - Never add explanations or extra text"""
                },
                {
                    "role": "user",
                    "content": f"Input Operation: {operation}\nInput Text: {text}"
                }
            ],
            temperature=0.1
        )
        
        response = completion.choices[0].message.content.strip()
        logger.info(f"Received response: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing string operation: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Test different operations
        tests = [
            ("reverse", "Hello World"),
            ("capitalize", "hello world"),
            ("count_words", "The quick brown fox"),
            ("remove_punctuation", "Hello, World! How are you?")
        ]
        
        for operation, text in tests:
            result = string_function(operation, text)
            print(f"\nOperation: {operation}")
            print(f"Input: {text}")
            print(f"Result: {result}")
            
    except Exception as e:
        logger.error(f"Failed to process: {str(e)}") 