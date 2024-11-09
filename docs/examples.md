# LLM Function Library Examples

## Basic Function Usage

### Math Function
```python
from basic_functions import math_function

# Basic arithmetic
result = math_function("2 + 2=")  # Returns: 4

# Percentages
result = math_function("What is 15% of 200?")  # Returns: 30

# Complex calculations
result = math_function("Square root of 16")  # Returns: 4
result = math_function("sin(90 degrees)")  # Returns: 1.0
```

### String Function
```python
from basic_functions import string_function

# Reverse text
result = string_function("reverse", "Hello World")  # Returns: dlroW olleH

# Capitalize text
result = string_function("capitalize", "hello world")  # Returns: HELLO WORLD

# Count words
result = string_function("count_words", "The quick brown fox")  # Returns: 4

# Remove punctuation
result = string_function("remove_punctuation", "Hello, World!")  # Returns: Hello World
```

### Vision Function
```python
from basic_functions import vision_function

# Generate image caption
caption = vision_function("caption", "path/to/image.jpg")

# Detailed analysis
analysis = vision_function("analyze", "path/to/image.jpg")

# Custom prompt
colors = vision_function(
    "custom", 
    "path/to/image.jpg", 
    "What are the dominant colors in this image?"
)
```

### Web Function
```python
from basic_functions import web_function

# Generate a login form
login_form = web_function(
    "form",
    "Create a login form with email and password",
    "modern"
)
print(login_form["html"])
print(login_form["css"])

# Create an animated button
button = web_function(
    "component",
    "Create a pulsing download button with icon",
    "minimal"
)
```

### Embedding Function
```python
from basic_functions import embedding_function

# Generate text embeddings
text = "The quick brown fox jumps over the lazy dog"
embedding = embedding_function(text)

# Use embeddings for similarity comparison
text1 = "I love programming"
text2 = "Coding is my passion"
embedding1 = embedding_function(text1)
embedding2 = embedding_function(text2)
```

### Debug Function
```python
from basic_functions import debug_function

# Analyze a runtime error
error_info = {
    'error_type': 'IndexError',
    'error_message': 'list index out of range',
    'traceback': """
        File "script.py", line 5
        print(numbers[5])
        IndexError: list index out of range
    """,
    'code_snippet': """
        numbers = [1, 2, 3]
        print(numbers[5])
    """,
    'variables': {
        'numbers': '[1, 2, 3]',
        'len(numbers)': '3'
    }
}

analysis = debug_function(error_info, "Error occurs during list access")
print(f"Analysis: {analysis['analysis']}")
print(f"Fix: {analysis['fix']}")
```

## Advanced Usage

### Code Review Application
```python
from applications.code_reviewer import analyze_code_file, generate_report

# Review a Python file
file_path = "path/to/your/code.py"
analysis = analyze_code_file(file_path)
report = generate_report(analysis)

# Save the report
with open("code_review.md", "w") as f:
    f.write(report)
```

### Function Chaining Example
```python
# Generate and analyze code
code = code_function("optimize", """
def factorial(n):
    if n == 0: return 1
    return n * factorial(n-1)
""")

# Debug the generated code
error_info = {
    'error_type': 'CodeReview',
    'error_message': 'Code Review',
    'code_snippet': code
}
analysis = debug_function(error_info)

# Generate documentation
docs = string_function("format_markdown", str(analysis))
```

## Best Practices
1. Always handle exceptions from LLM functions
2. Use appropriate temperature settings for different tasks
3. Provide clear, specific prompts
4. Validate outputs when needed
5. Consider rate limits and API usage 