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

def embedding_function(text: str) -> list:
    """
    Generate embeddings for input text using Ollama's embedding models.
    
    Args:
        text (str): Text to generate embeddings for
        
    Returns:
        list: Vector embedding
        
    Raises:
        Exception: If API call fails
    """
    try:
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        
        logger.info(f"Generating embeddings for text: {text[:100]}...")
        
        # Using nomic-embed-text model which is optimized for embeddings
        response = client.embeddings.create(
            model="nomic-embed-text",
            input=text
        )
        
        embedding = response.data[0].embedding
        logger.info(f"Generated embedding vector of length: {len(embedding)}")
        return embedding
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        sample_text = "This is a test sentence to generate embeddings."
        embedding = embedding_function(sample_text)
        print(f"Generated embedding vector (first 5 values): {embedding[:5]}")
    except Exception as e:
        logger.error(f"Failed to process: {str(e)}") 