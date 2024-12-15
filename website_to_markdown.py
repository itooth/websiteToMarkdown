import requests
import os
import time
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load environment variables
load_dotenv()

def create_session_with_retries():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    
    # Define retry strategy
    retries = Retry(
        total=3,  # reduced number of retries
        backoff_factor=1,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST"]
    )
    
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def is_yuque_url(url):
    return 'yuque.com' in url.lower()

def convert_to_markdown(url):
    try:
        # Headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("FIRECRAWL_API_KEY")}'
        }
        
        # Create session with retry mechanism
        session = create_session_with_retries()
        
        # Use scrape endpoint with actions for Yuque URLs
        api_url = "https://api.firecrawl.dev/v1/scrape"
        
        if is_yuque_url(url):
            data = {
                "url": url,
                "formats": ["markdown"],
                "actions": [
                    {"type": "wait", "milliseconds": 3000},  # Initial wait for page load
                    {"type": "executeJavascript", "script": "document.querySelector('article') !== null"},  # Check if article exists
                    {"type": "wait", "milliseconds": 1000},  # Wait after check
                    {"type": "scroll", "direction": "down", "distance": 500},  # Scroll to trigger lazy loading
                    {"type": "wait", "milliseconds": 1000},  # Wait after scroll
                    {"type": "scroll", "direction": "down", "distance": 1000},  # Scroll more
                    {"type": "wait", "milliseconds": 1000}  # Final wait
                ]
            }
        else:
            data = {
                "url": url,
                "formats": ["markdown"]
            }
        
        # Make the request
        print(f"Making scrape request to Firecrawl with data: {data}")
        response = session.post(api_url, headers=headers, json=data, timeout=30)  # Reduced timeout since we're using actions
        
        # Print full response for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print("Response JSON:", response_json)
        except Exception as e:
            print(f"Failed to parse response as JSON: {str(e)}")
            print("Raw response:", response.text)
            return None
        
        if response_json.get('success'):
            return response_json['data']['markdown']
        else:
            error_msg = response_json.get('error', 'Unknown error')
            details = response_json.get('details', [])
            if details and isinstance(details, list):
                error_msg = f"{error_msg}: {'; '.join(str(d) for d in details)}"
            print(f"API Error: {error_msg}")
            return None
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Get URL from user
    url = input("Enter the website URL to convert to markdown: ")
    
    # Convert to markdown
    markdown = convert_to_markdown(url)
    
    if markdown:
        # Save to file
        output_file = "output.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"\nMarkdown has been saved to {output_file}")
    else:
        print("\nFailed to convert the webpage to markdown.") 