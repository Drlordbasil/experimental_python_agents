# LLM-Powered Function Library: Reimagining Software Functions as Language Models

## Project Structure
```
experimental_python_agents/
├── README.md                 # Project overview and documentation
├── config.py                 # Configuration for LLM models and logging
├── main.py                  # Main showcase of all functions
├── requirements.txt         # Project dependencies
├── basic_functions/        # Core LLM Function Agents
│   ├── __init__.py
│   ├── math_function.py    # Mathematical operations
│   ├── string_function.py  # String manipulations
│   ├── embedding_function.py # Text embeddings
│   ├── vision_function.py  # Image analysis
│   ├── web_function.py     # Web component generation
│   └── debug_function.py   # Error analysis
└── applications/           # Practical Implementations
    └── code_reviewer/     # Code review system
        ├── reviewer.py
        ├── test_reviewer.py
        └── reports/
```

## Core Concept
This project reimagines traditional programming functions as LLM-powered agents. Instead of writing static functions, we use LLMs to create dynamic, context-aware operations that adapt to input and provide intelligent outputs.

## Current Functions

### Basic Functions
1. **Math Function** (`math_function.py`)
   - Natural language math processing
   - Direct numerical output
   - Example: `math_function("What is 15% of 200?")`

2. **String Function** (`string_function.py`)
   - Text transformations (reverse, capitalize)
   - Word counting
   - Punctuation handling
   - Example: `string_function("reverse", "Hello World")`

3. **Vision Function** (`vision_function.py`)
   - Image analysis and captioning
   - Uses llama3.2-vision:11b model
   - Example: `vision_function("analyze", "image.png")`

4. **Web Function** (`web_function.py`)
   - HTML/CSS generation
   - Component creation
   - Example: `web_function("component", "Create a login form")`

5. **Embedding Function** (`embedding_function.py`)
   - Text vectorization using nomic-embed-text
   - Example: `embedding_function("Convert this text to vectors")`

6. **Debug Function** (`debug_function.py`)
   - Error analysis and solutions
   - Root cause identification
   - Example: `debug_function(error_info, context)`

### Applications

#### Code Review System
- Located in `applications/code_reviewer/`
- Analyzes code quality
- Suggests optimizations
- Generates documentation
- Creates markdown reports

## Requirements
- Python 3.x
- Ollama running locally
- OpenAI library for API structure
- Required Ollama models:
  - smollm2:1.7b (text generation)
  - llama3.2-vision:11b (vision processing)
  - nomic-embed-text (embeddings)

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Pull required Ollama models
ollama pull smollm2:1.7b
ollama pull llama3.2-vision:11b
ollama pull nomic-embed-text
```

## Usage Example
```python
from basic_functions import math_function, string_function, vision_function

# Math operations
result = math_function("2 + 2=")
print(f"Math result: {result}")

# String operations
text = string_function("reverse", "Hello World")
print(f"Reversed text: {text}")

# Image analysis
description = vision_function("caption", "image.png")
print(f"Image caption: {description}")
```

## Future Development
1. Enhanced error handling
2. Additional function agents
3. More practical applications
4. Performance optimizations
5. Extended documentation