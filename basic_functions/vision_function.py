from openai import OpenAI
import logging
import sys
from pathlib import Path
import base64

# Add root directory to Python path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from config import OLLAMA_CONFIG, LOG_CONFIG

# Configure logging
logging.basicConfig(level=LOG_CONFIG["level"], format=LOG_CONFIG["format"])
logger = logging.getLogger(__name__)

def encode_image(image_path):
    """Convert image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def vision_function(operation: str, image_path: str, prompt: str = None) -> str:
    """
    Process images using LLM vision model.
    
    Args:
        operation (str): Operation to perform (e.g., 'caption', 'analyze', 'describe')
        image_path (str): Path to image file
        prompt (str, optional): Custom prompt for image analysis
        
    Returns:
        str: Generated description/analysis
        
    Raises:
        Exception: If API call fails
    """
    try:
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        
        logger.info(f"Processing vision operation: {operation} on image: {image_path}")
        
        # Encode image to base64
        base64_image = encode_image(image_path)
        
        # Default prompts for different operations
        operation_prompts = {
            "caption": "Generate a short, accurate caption for this image.",
            "analyze": "Provide a detailed analysis of this image.",
            "describe": "Describe what you see in this image.",
        }
        
        # Use custom prompt if provided, otherwise use default
        content = prompt if prompt else operation_prompts.get(operation, "What is in this image?")
        
        completion = client.chat.completions.create(
            model=OLLAMA_CONFIG["vision_model"],
            messages=[
                {
                    "role": "system", 
                    "content": "You are a precise image analysis model. Respond with accurate, factual descriptions only."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": content
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1
        )
        
        response = completion.choices[0].message.content.strip()
        logger.info("Vision processing completed")
        return response
        
    except Exception as e:
        logger.error(f"Error processing vision operation: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Test different operations
        test_image = "image.png"
        
        operations = [
            ("caption", None),
            ("analyze", None),
            ("describe", None),
            ("custom", "What colors are most prominent in this image?")
        ]
        
        for op, prompt in operations:
            result = vision_function(op, test_image, prompt)
            print(f"\nOperation: {op}")
            print(f"Result: {result}")
            print("-" * 50)
            
    except Exception as e:
        logger.error(f"Failed to process: {str(e)}") 