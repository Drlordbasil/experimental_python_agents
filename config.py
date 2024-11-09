# LLM Configuration
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
    "model": "smollm2:1.7b",
    "temperature": 0.1,
    "embedding_model": "nomic-embed-text"
}

# Logging Configuration
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
} 