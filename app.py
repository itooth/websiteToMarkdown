from flask import Flask, render_template, request, jsonify, session
import markdown2
from website_to_markdown import convert_to_markdown
from prompts import CLEANING_PROMPT_TEMPLATE
import re
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Enable hot reloading and disable template caching in development
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Password for AI cleaning
AI_PASSWORD = "9382"
CONVERSIONS_LIMIT = 5

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form.get('password')
    if password == AI_PASSWORD:
        session['conversions_count'] = 0  # Reset count when password is correct
        return jsonify({'success': True})
    return jsonify({'success': False})

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
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4000
            },
            timeout=60
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
    # Initialize conversions count if not exists
    if 'conversions_count' not in session:
        session['conversions_count'] = 0
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
                # Check conversions count
                conversions_count = session.get('conversions_count', 0)
                needs_password = conversions_count >= CONVERSIONS_LIMIT
                
                # Clean the markdown using AI if allowed
                if needs_password:
                    cleaned_markdown = markdown_content  # Don't clean if password needed
                    requires_password = True
                else:
                    cleaned_markdown = clean_markdown_with_ai(markdown_content, url)
                    session['conversions_count'] = conversions_count + 1
                    requires_password = False
                
                # Convert both original and cleaned markdown to HTML for preview
                html_content = markdown2.markdown(markdown_content)
                cleaned_html = markdown2.markdown(cleaned_markdown) if cleaned_markdown else None
                
                # Extract title from markdown content
                title = "Untitled"
                title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                
                # Get the cleaning prompt with the actual markdown content
                current_cleaning_prompt = CLEANING_PROMPT_TEMPLATE.format(markdown_content=markdown_content)
                
                return jsonify({
                    'success': True,
                    'markdown': markdown_content,
                    'html': html_content,
                    'cleaned_markdown': cleaned_markdown,
                    'cleaned_html': cleaned_html,
                    'title': title,
                    'cleaning_prompt': current_cleaning_prompt,
                    'requires_password': requires_password
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