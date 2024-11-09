from typing import Dict, List
import sys
from pathlib import Path

# Add root directory to Python path
root_dir = str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from basic_functions.code_function import code_function
from basic_functions.debug_function import debug_function
from basic_functions.string_function import string_function

def analyze_code_file(file_path: str) -> Dict[str, any]:
    """Analyze a code file using LLM functions."""
    with open(file_path, 'r') as f:
        code = f.read()
    
    # Get optimized version
    optimized = code_function("optimize", code)
    
    # Get potential issues
    error_info = {
        'error_type': 'CodeReview',
        'error_message': 'Code Review Analysis',
        'traceback': '',  # Not applicable for code review
        'code_snippet': code,
        'variables': {
            'file_path': file_path,
            'code_length': len(code),
            'review_type': 'static_analysis'
        }
    }
    issues = debug_function(error_info, "Perform a comprehensive code review focusing on optimization, security, and best practices")
    
    # Generate documentation
    docs = code_function("document", code)
    
    return {
        "original": code,
        "optimized": optimized,
        "issues": issues,
        "documentation": docs
    }

def generate_report(analysis: Dict[str, any], output_format: str = "markdown") -> str:
    """Generate formatted report from analysis results."""
    report = f"""
# Code Analysis Report

## Original Code
```python
{analysis['original']}
```

## Optimized Version
```python
{analysis['optimized']}
```

## Issues Found
- Analysis: {analysis['issues']['analysis']}
- Root Cause: {analysis['issues']['root_cause']}
- Suggested Fix: {analysis['issues']['fix']}
- Prevention: {analysis['issues']['prevention']}

## Documentation
```python
{analysis['documentation']}
```
"""
    
    if output_format != "markdown":
        report = string_function("convert_format", report)
    
    return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reviewer.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    analysis = analyze_code_file(file_path)
    report = generate_report(analysis)
    print(report) 