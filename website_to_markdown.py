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
        total=5,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[408, 429, 500, 502, 503, 504],  # retry on these status codes
        allowed_methods=["HEAD", "GET", "POST"]  # allow retries on these methods
    )
    
    # Mount the adapter with retry strategy for both http and https
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
        
        if is_yuque_url(url):
            # Use crawl endpoint for Yuque URLs
            api_url = "https://api.firecrawl.dev/v1/crawl"
            data = {
                "url": url,
                "limit": 1,  # Only get the current page
                "scrapeOptions": {
                    "formats": ["markdown"]
                }
            }
            
            # Submit crawl job with retry mechanism
            print(f"Making crawl request to Firecrawl with data: {data}")
            response = session.post(api_url, headers=headers, json=data, timeout=90)  # Increased timeout
            
            if response.status_code == 200:
                crawl_response = response.json()
                if crawl_response.get('success'):
                    crawl_id = crawl_response['id']
                    status_url = f"https://api.firecrawl.dev/v1/crawl/{crawl_id}"
                    
                    # Poll for results with exponential backoff
                    max_attempts = 10
                    for attempt in range(max_attempts):
                        wait_time = min(30, 2 ** attempt)  # Exponential backoff, max 30 seconds
                        print(f"Checking crawl status (attempt {attempt + 1}/{max_attempts}), waiting {wait_time} seconds")
                        time.sleep(wait_time)
                        
                        status_response = session.get(status_url, headers=headers)
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            if status_data.get('status') == 'completed' and status_data.get('data'):
                                # Return the first page's markdown
                                return status_data['data'][0]['markdown']
                            elif status_data.get('status') == 'failed':
                                print(f"Crawl failed: {status_data.get('error')}")
                                return None
                    
                    print("Crawl timed out after maximum attempts")
                    return None
            else:
                error_msg = response.json().get('error', 'Unknown error')
                print(f"Crawl API Error: {error_msg}")
                return None
        else:
            # Use scrape endpoint for non-Yuque URLs
            api_url = "https://api.firecrawl.dev/v1/scrape"
            data = {
                "url": url,
                "formats": ["markdown"]
            }
            
            # Make the request with retry mechanism
            print(f"Making scrape request to Firecrawl with data: {data}")
            response = session.post(api_url, headers=headers, json=data, timeout=90)  # Increased timeout
            
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