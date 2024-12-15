import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def convert_to_markdown(url):
    try:
        # API endpoint
        api_url = "https://api.firecrawl.dev/v1/scrape"
        
        # Headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("FIRECRAWL_API_KEY")}'
        }
        
        # Request body - keeping it minimal
        data = {
            "url": url,
            "formats": ["markdown"]
        }
        
        # Make the request
        print(f"Making request to Firecrawl with data: {data}")  # Debug print
        response = requests.post(api_url, headers=headers, json=data)
        
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