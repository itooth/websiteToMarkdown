from flask import Flask, render_template, request, jsonify
import markdown2
from website_to_markdown import convert_to_markdown
import re
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable hot reloading and disable template caching in development
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# Define cleaning prompt template
CLEANING_PROMPT_TEMPLATE = """You will be given a page of text extracted from an open source project development guide. The text may contain irrelevant parts due to the extraction process. Your task is to clean up the text, remove irrelevant parts, and format it into Markdown.

Here is the extracted text:

<text>
{markdown_content}
</text>

Follow these steps to clean up and format the text:

1. Remove any irrelevant parts, such as navigation elements, comments, or unrelated content.
2. Keep only the main content related to the topic of the page.
3. Format the text into proper Markdown, including:
   - Use appropriate heading levels (# for main title, ## for subtitles, etc.)
   - Format code blocks using triple backticks (```) with the appropriate language specified
   - Use proper Markdown syntax for lists, bold text, and other formatting elements

Your output should be structured like this:

```markdown
# Main Title

## Subtitle (if applicable)

Main content paragraphs...

### Subsection (if applicable)

More content...

```code example```

Additional content...
```

Ensure that the final output is clean, well-formatted Markdown that accurately represents the main content of the original text.

Provide your cleaned and formatted Markdown output inside <cleaned_markdown> tags."""

def clean_markdown_with_ai(markdown_content, webpage_url):
    try:
        # ChatAnywhere API endpoint
        api_url = "https://api.chatanywhere.tech/v1/chat/completions"
        
        # Create the cleaning prompt with the actual markdown content
        cleaning_prompt = CLEANING_PROMPT_TEMPLATE.format(markdown_content=markdown_content)
        
        # Prepare the messages for the API
        messages = [
            {"role": "system", "content": "You are a helpful assistant that cleans and formats markdown content."},
            {"role": "user", "content": cleaning_prompt}
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

        if response.status_code == 200:
            ai_response = response.json()
            assistant_message = ai_response['choices'][0]['message']['content']
            
            # Extract content between <cleaned_markdown> tags
            cleaned_match = re.search(r'<cleaned_markdown>(.*?)</cleaned_markdown>', 
                                    assistant_message, re.DOTALL)
            
            if cleaned_match:
                return cleaned_match.group(1).strip()
            else:
                return assistant_message  # Return full response if tags not found
        else:
            print(f"AI API Error: {response.text}")
            return markdown_content  # Return original content if AI cleaning fails

    except Exception as e:
        print(f"Error in AI cleaning: {str(e)}")
        return markdown_content  # Return original content if AI cleaning fails

@app.route('/')
def index():
    return render_template('index.html', cleaning_prompt=CLEANING_PROMPT_TEMPLATE)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        print(f"Converting URL: {url}")  # Debug print
        markdown_content = convert_to_markdown(url)
        
        if markdown_content:
            try:
                # Clean the markdown using AI
                cleaned_markdown = clean_markdown_with_ai(markdown_content, url)
                
                # Convert both original and cleaned markdown to HTML for preview
                html_content = markdown2.markdown(markdown_content)
                cleaned_html = markdown2.markdown(cleaned_markdown) if cleaned_markdown else None
                
                # Extract title from markdown content
                title = "Untitled"
                title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                
                # Get the cleaning prompt with the actual URL
                current_cleaning_prompt = CLEANING_PROMPT_TEMPLATE.format(markdown_content=markdown_content)
                
                return jsonify({
                    'success': True,
                    'markdown': markdown_content,
                    'html': html_content,
                    'cleaned_markdown': cleaned_markdown,
                    'cleaned_html': cleaned_html,
                    'title': title,
                    'cleaning_prompt': current_cleaning_prompt
                })
            except Exception as e:
                print(f"Error in markdown processing: {str(e)}")
                return jsonify({
                    'success': True,
                    'markdown': markdown_content,
                    'html': markdown2.markdown(markdown_content),
                    'title': 'Untitled',
                    'cleaning_prompt': CLEANING_PROMPT_TEMPLATE.format(markdown_content=markdown_content)
                })
        else:
            return jsonify({
                'error': 'Failed to convert webpage to markdown. Please check if the URL is accessible.'
            }), 400
    
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 