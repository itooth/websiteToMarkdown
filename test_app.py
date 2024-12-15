import unittest
from website_to_markdown import convert_to_markdown
from app import app, clean_markdown_with_ai
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

class TestWebsiteToMarkdown(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.test_urls = [
            {
                "name": "Yuque Document",
                "url": "https://wflow.yuque.com/org-wiki-wflow-yb1yv4/vna85l/gd0nmmrgg56w2pm2"
            },
            {
                "name": "Example Website",
                "url": "https://example.com"
            },
            {
                "name": "Mozilla Developer",
                "url": "https://developer.mozilla.org/en-US/docs/Web/Markdown"
            }
        ]

    def test_firecrawl_api_key(self):
        """Test if Firecrawl API key is set"""
        api_key = os.getenv('FIRECRAWL_API_KEY')
        self.assertIsNotNone(api_key, "Firecrawl API key not found in environment variables")
        self.assertTrue(api_key.startswith('fc-'), "Invalid Firecrawl API key format")

    def test_chatanywhere_api_key(self):
        """Test if ChatAnywhere API key is set"""
        api_key = os.getenv('CHATANYWHERE_API_KEY')
        self.assertIsNotNone(api_key, "ChatAnywhere API key not found in environment variables")
        self.assertTrue(api_key.startswith('sk-'), "Invalid ChatAnywhere API key format")

    def test_url_accessibility(self):
        """Test if URLs are accessible"""
        print("\nTesting URL accessibility...")
        for test_case in self.test_urls:
            print(f"\nChecking URL: {test_case['name']}")
            try:
                response = requests.get(test_case['url'])
                print(f"Status code: {response.status_code}")
                print(f"Headers: {dict(response.headers)}")
                self.assertIn(response.status_code, [200, 301, 302], f"URL {test_case['url']} is not accessible")
            except Exception as e:
                print(f"Error accessing URL: {str(e)}")
                self.fail(f"Failed to access {test_case['url']}: {str(e)}")

    def test_convert_to_markdown_function(self):
        """Test the convert_to_markdown function with different URLs"""
        print("\nTesting convert_to_markdown function...")
        for test_case in self.test_urls:
            print(f"\nTesting URL: {test_case['name']}")
            print(f"URL: {test_case['url']}")
            
            result = convert_to_markdown(test_case['url'])
            print(f"Result: {'Success' if result else 'Failed'}")
            if result:
                print(f"Content length: {len(result)} characters")
                print("First 200 characters:")
                print(result[:200])
            else:
                print("No content returned")
                print("Testing direct API call...")
                # Test direct API call for debugging
                api_url = "https://api.firecrawl.dev/v1/scrape"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {os.getenv("FIRECRAWL_API_KEY")}'
                }
                data = {
                    "url": test_case['url'],
                    "formats": ["markdown"]
                }
                try:
                    response = requests.post(api_url, headers=headers, json=data)
                    print(f"Direct API Response: {response.text}")
                except Exception as e:
                    print(f"Direct API Error: {str(e)}")
            
            self.assertIsNotNone(result, f"Failed to convert {test_case['name']} to markdown")

    def test_clean_markdown_with_ai(self):
        """Test the AI cleaning functionality"""
        print("\nTesting AI cleaning functionality...")
        test_markdown = """# Test Title
<div>Some HTML content</div>
## Section 1
* List item 1
* List item 2
<footer>Footer content</footer>"""

        result = clean_markdown_with_ai(test_markdown, "https://example.com")
        print("\nInput markdown:")
        print(test_markdown)
        print("\nCleaned markdown:")
        print(result)
        
        self.assertIsNotNone(result, "AI cleaning returned None")
        self.assertNotIn("<div>", result, "HTML tags not removed")
        self.assertNotIn("<footer>", result, "HTML tags not removed")

    def test_web_interface(self):
        """Test the web interface endpoints"""
        print("\nTesting web interface...")
        
        # Test home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200, "Home page not accessible")
        
        # Test conversion endpoint
        test_url = self.test_urls[0]['url']
        print(f"\nTesting conversion endpoint with URL: {test_url}")
        response = self.app.post('/convert', data={'url': test_url})
        
        # Print response details for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        try:
            json_data = response.get_json()
            print("Response data:", json_data)
        except Exception as e:
            print(f"Failed to parse response as JSON: {str(e)}")
            print("Raw response:", response.data.decode())
            raise
        
        self.assertEqual(response.status_code, 200, "Conversion endpoint failed")
        self.assertTrue(json_data.get('success'), "Conversion not successful")
        self.assertIsNotNone(json_data.get('markdown'), "No markdown in response")
        self.assertIsNotNone(json_data.get('cleaned_markdown'), "No cleaned markdown in response")

def run_tests():
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWebsiteToMarkdown)
    
    # Run the tests
    print("=== Starting Website to Markdown Tests ===")
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_tests() 