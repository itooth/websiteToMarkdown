import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ai_cleaning(markdown_content, webpage_url):
    try:
        # ChatAnywhere API endpoint
        api_url = "https://api.chatanywhere.tech/v1/chat/completions"
        
        # Comprehensive cleaning prompt
        cleaning_prompt = """Please clean and format this markdown content following these rules:

1. Remove any HTML tags
2. Clean up unnecessary whitespace and line breaks
3. Ensure proper markdown formatting:
   - Use '#' for main title
   - Use '##' for section headings
   - Format code blocks with ```
   - Use proper list formatting
   - Preserve links and images
4. Return the cleaned content between <cleaned_markdown> tags

The content should be clean, well-formatted, and easy to read."""

        # Prepare the messages for the API
        messages = [
            {"role": "system", "content": "You are a helpful assistant that cleans and formats markdown content."},
            {"role": "user", "content": f"Here is the markdown content to clean:\n\n{markdown_content}\n\nPlease follow these instructions:\n\n{cleaning_prompt}"}
        ]

        # Make the API request
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {os.getenv('CHATANYWHERE_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=30
        )

        print("\nAPI Response Status:", response.status_code)
        print("API Response:", response.text)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

def run_tests():
    # Test cases
    test_cases = [
        {
            "name": "Simple Markdown",
            "markdown": """# Test Title
This is a simple test.
* List item 1
* List item 2""",
            "url": "https://example.com/test1"
        },
        {
            "name": "HTML Mixed Content",
            "markdown": """<header>Header</header>
# Main Title
<nav>Navigation</nav>
## Section 1
This is the main content.
<div class="sidebar">Sidebar content</div>
* Item 1
* Item 2
<footer>Footer</footer>""",
            "url": "https://example.com/test2"
        },
        {
            "name": "Code Blocks and Links",
            "markdown": """# Code Example
Here's some code:
```python
def hello():
    print("Hello World")
```
Check out this [link](https://example.com)
And an image: ![alt text](image.jpg)""",
            "url": "https://example.com/test3"
        }
    ]

    print("\n=== Starting AI Cleaning Tests ===\n")

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test['name']}")
        print("-" * 50)
        print("\nInput Markdown:")
        print(test['markdown'])
        print("\nProcessing...")
        
        result = test_ai_cleaning(test['markdown'], test['url'])
        print("\nResult:")
        print(result)
        
        if result and not result.startswith('Error'):
            print("\n✅ Test passed")
        else:
            print("\n❌ Test failed")
            print("Error:", result)
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv('CHATANYWHERE_API_KEY'):
        print("Error: CHATANYWHERE_API_KEY not found in environment variables")
        exit(1)
    
    run_tests() 