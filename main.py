from openai import OpenAI
import logging
from pathlib import Path
from typing import Any, Dict
import base64

from basic_functions.math_function import math_function
from basic_functions.string_function import string_function
from basic_functions.code_function import code_function
from basic_functions.embedding_function import embedding_function
from basic_functions.vision_function import vision_function
from basic_functions.web_function import web_function
from basic_functions.debug_function import debug_function
from config import LOG_CONFIG

# Configure logging
logging.basicConfig(level=LOG_CONFIG["level"], format=LOG_CONFIG["format"])
logger = logging.getLogger(__name__)

def showcase_math():
    logger.info("=== Math Function Showcase ===")
    expressions = [
        "2 + 2=",
        "Square root of 16",
        "15% of 200",
        "sin(90 degrees)"
    ]
    
    for expr in expressions:
        result = math_function(expr)
        print(f"\nExpression: {expr}")
        print(f"Result: {result}")

def showcase_string():
    logger.info("=== String Function Showcase ===")
    tests = [
        ("reverse", "Hello World"),
        ("capitalize", "python programming"),
        ("count_words", "The quick brown fox jumps over the lazy dog"),
        ("remove_punctuation", "Hello, World! How are you???")
    ]
    
    for operation, text in tests:
        result = string_function(operation, text)
        print(f"\nOperation: {operation}")
        print(f"Input: {text}")
        print(f"Result: {result}")

def showcase_code():
    logger.info("=== Code Function Showcase ===")
    test_code = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
    """
    
    operations = ["optimize", "add_typing", "add_tests"]
    for op in operations:
        result = code_function(op, test_code)
        print(f"\nOperation: {op}")
        print("Result:")
        print(result)

def showcase_embedding():
    logger.info("=== Embedding Function Showcase ===")
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is fascinating"
    ]
    
    for text in texts:
        embedding = embedding_function(text)
        print(f"\nText: {text}")
        print(f"Embedding (first 5 dimensions): {embedding[:5]}")

def showcase_vision():
    logger.info("=== Vision Function Showcase ===")
    # Make sure this image exists in your project
    image_path = "image.png"
    
    operations = [
        ("caption", None),
        ("analyze", None),
        ("custom", "What emotions are expressed in this image?")
    ]
    
    for op, prompt in operations:
        result = vision_function(op, image_path, prompt)
        print(f"\nOperation: {op}")
        print(f"Result: {result}")

def showcase_web():
    logger.info("=== Web Function Showcase ===")
    components = [
        ("component", "Create a modern social media share button with animation", "modern"),
        ("form", "Create a contact form with name, email, and message", "minimal")
    ]
    
    for op, content, style in components:
        result = web_function(op, content, style)
        print(f"\nComponent: {content}")
        print("HTML:")
        print(result["html"])
        print("\nCSS:")
        print(result["css"])

def showcase_debug():
    logger.info("=== Debug Function Showcase ===")
    error_info = {
        'error_type': 'TypeError',
        'error_message': "can't multiply sequence by non-int of type 'str'",
        'traceback': """Traceback (most recent call last):
  File "script.py", line 3, in <module>
    result = [1, 2, 3] * "2"
TypeError: can't multiply sequence by non-int of type 'str'""",
        'code_snippet': """numbers = [1, 2, 3]
multiplier = "2"
result = numbers * multiplier""",
        'variables': {
            'numbers': '[1, 2, 3]',
            'multiplier': '"2"',
            'type(multiplier)': "<class 'str'>"
        }
    }
    
    result = debug_function(error_info, "Error occurred during list multiplication")
    print("\nDebug Analysis:")
    for section, content in result.items():
        print(f"\n{section.upper()}:")
        print(content)

def main():
    try:
        print("\n=== LLM Function Library Showcase ===\n")
        
        # Basic operations
        showcase_math()
        showcase_string()
        
        # Code operations
        showcase_code()
        showcase_debug()
        
        # Media operations
        showcase_vision()
        
        # Web operations
        showcase_web()
        
        # Data operations
        showcase_embedding()
        
    except Exception as e:
        logger.error(f"Showcase failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 