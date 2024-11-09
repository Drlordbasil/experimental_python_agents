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

def code_function(operation: str, code: str, language: str = "python") -> str:
    """
    Process code operations using LLM.
    
    Args:
        operation (str): Operation to perform (e.g., 'optimize', 'add_typing', 'add_tests', 'document', 'refactor')
        code (str): Code to process
        language (str): Programming language of the code
        
    Returns:
        str: Processed code
        
    Raises:
        Exception: If API call fails
    """
    try:
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        
        logger.info(f"Processing code operation: {operation} for {language} code...")
        
        completion = client.chat.completions.create(
            model=OLLAMA_CONFIG["model"],
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are an expert {language} developer. You modify code based on requested operations.
                    ONLY output the modified code with NO explanations.
                    
                    Examples:
                    Input Operation: optimize
                    Input Code: 
                    def factorial(n):
                        if n == 0: return 1
                        return n * factorial(n-1)
                    Output:
                    def factorial(n):
                        result = 1
                        for i in range(1, n + 1):
                            result *= i
                        return result
                    
                    Input Operation: add_typing
                    Input Code:
                    def merge_lists(list1, list2):
                        return sorted(list1 + list2)
                    Output:
                    def merge_lists(list1: list[int], list2: list[int]) -> list[int]:
                        return sorted(list1 + list2)
                    
                    Input Operation: add_tests
                    Input Code:
                    def is_palindrome(s):
                        return s == s[::-1]
                    Output:
                    def is_palindrome(s: str) -> bool:
                        return s == s[::-1]

                    def test_is_palindrome():
                        assert is_palindrome("radar") == True
                        assert is_palindrome("hello") == False
                        assert is_palindrome("") == True
                        assert is_palindrome("a") == True
                        print("All palindrome tests passed!")
                    
                    IMPORTANT:
                    - Return ONLY the modified code
                    - Preserve functionality while improving code
                    - Follow language best practices
                    - No comments or explanations in output"""
                },
                {
                    "role": "user",
                    "content": f"Input Operation: {operation}\nInput Code:\n{code}"
                }
            ],
            temperature=0.1
        )
        
        response = completion.choices[0].message.content.strip()
        logger.info("Code processing completed")
        return response
        
    except Exception as e:
        logger.error(f"Error processing code operation: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Test different operations
        test_code = """
def calculate_average(numbers):
    sum = 0
    for n in numbers:
        sum += n
    return sum / len(numbers)
        """
        
        operations = ["optimize", "add_typing", "add_tests", "document"]
        
        for op in operations:
            result = code_function(op, test_code)
            print(f"\nOperation: {op}")
            print("Result:")
            print(result)
            print("-" * 50)
            
    except Exception as e:
        logger.error(f"Failed to process: {str(e)}") 