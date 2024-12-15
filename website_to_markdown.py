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
        
        # Request body
        data = {
            "url": url,
            "formats": ["markdown"]
        }
        
        # Make the request
        response = requests.post(api_url, headers=headers, json=data)
        response_json = response.json()
        
        if response_json.get('success'):
            return response_json['data']['markdown']
        else:
            print(f"API Error: {response_json}")
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