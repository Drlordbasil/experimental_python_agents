from openai import OpenAI
import logging
import sys
from pathlib import Path
import re
from bs4 import BeautifulSoup

# Add root directory to Python path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from config import OLLAMA_CONFIG, LOG_CONFIG

# Configure logging
logging.basicConfig(level=LOG_CONFIG["level"], format=LOG_CONFIG["format"])
logger = logging.getLogger(__name__)

def web_function(operation: str, content: str, style: str = "modern") -> dict:
    """
    Generate and validate web components using LLM.
    
    Args:
        operation (str): Operation to perform (e.g., 'component', 'form', 'layout', 'animation')
        content (str): Description of what to generate
        style (str): Design style preference
        
    Returns:
        dict: Contains HTML, CSS, and validation results
        
    Raises:
        Exception: If API call fails or validation fails
    """
    try:
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        
        logger.info(f"Processing web operation: {operation} with style: {style}")
        
        completion = client.chat.completions.create(
            model=OLLAMA_CONFIG["model"],
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are an expert web developer. Generate valid HTML5 and CSS3 based on descriptions.
                    Return ONLY the code in this format:
                    ---HTML---
                    <your html here>
                    ---CSS---
                    <your css here>
                    
                    Examples:
                    Input Operation: component
                    Input Content: Create a notification bell icon that shows unread count
                    Style: modern
                    Output:
                    ---HTML---
                    <div class="notification-bell">
                        <i class="bell-icon">🔔</i>
                        <span class="notification-count">3</span>
                    </div>
                    ---CSS---
                    .notification-bell {{
                        position: relative;
                        cursor: pointer;
                    }}
                    .bell-icon {{
                        font-size: 24px;
                    }}
                    .notification-count {{
                        position: absolute;
                        top: -8px;
                        right: -8px;
                        background: #ff4444;
                        color: white;
                        border-radius: 50%;
                        padding: 2px 6px;
                        font-size: 12px;
                    }}
                    
                    Input Operation: form
                    Input Content: Create a login form with email and password
                    Style: minimal
                    Output:
                    ---HTML---
                    <form class="login-form">
                        <input type="email" placeholder="Email" required>
                        <input type="password" placeholder="Password" required>
                        <button type="submit">Login</button>
                    </form>
                    ---CSS---
                    .login-form {{
                        display: flex;
                        flex-direction: column;
                        gap: 1rem;
                        max-width: 300px;
                    }}
                    input {{
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }}
                    button {{
                        padding: 8px;
                        background: #007bff;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }}
                    
                    IMPORTANT:
                    - Generate semantic HTML5
                    - Use modern CSS features
                    - Ensure accessibility
                    - Keep it responsive
                    - Follow {style} design principles"""
                },
                {
                    "role": "user",
                    "content": f"Input Operation: {operation}\nInput Content: {content}\nStyle: {style}"
                }
            ],
            temperature=0.1
        )
        
        response = completion.choices[0].message.content.strip()
        
        # Parse response
        html_match = re.search(r'---HTML---\n(.*?)\n---CSS---', response, re.DOTALL)
        css_match = re.search(r'---CSS---\n(.*?)$', response, re.DOTALL)
        
        if not html_match or not css_match:
            raise ValueError("Invalid response format")
            
        html = html_match.group(1).strip()
        css = css_match.group(1).strip()
        
        # Validate HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Basic validation
        validation = {
            "valid_html": True,
            "warnings": [],
            "accessibility": []
        }
        
        # Check for basic accessibility
        for img in soup.find_all('img'):
            if not img.get('alt'):
                validation["accessibility"].append("Image missing alt text")
                
        for input in soup.find_all('input'):
            if not input.get('aria-label') and not input.get('placeholder'):
                validation["accessibility"].append("Input missing label or placeholder")
        
        logger.info("Web component generated and validated")
        
        return {
            "html": html,
            "css": css,
            "validation": validation
        }
        
    except Exception as e:
        logger.error(f"Error processing web operation: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Test different operations
        tests = [
            ("component", "Create a pulsing download button with icon", "modern"),
            ("form", "Create a newsletter signup with name and email", "minimal"),
            ("layout", "Create a card grid layout for blog posts", "modern")
        ]
        
        for operation, content, style in tests:
            result = web_function(operation, content, style)
            print(f"\nOperation: {operation}")
            print("HTML:")
            print(result["html"])
            print("\nCSS:")
            print(result["css"])
            print("\nValidation:")
            print(result["validation"])
            print("-" * 50)
            
    except Exception as e:
        logger.error(f"Failed to process: {str(e)}") 