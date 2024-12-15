from flask import Flask, render_template, request, jsonify
import markdown2
from website_to_markdown import convert_to_markdown
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    markdown_content = convert_to_markdown(url)
    if markdown_content:
        # Convert markdown to HTML for preview
        html_content = markdown2.markdown(markdown_content)
        
        # Extract title from markdown content
        title = "Untitled"
        # Try to find a title in the markdown content
        title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        
        return jsonify({
            'success': True,
            'markdown': markdown_content,
            'html': html_content,
            'title': title
        })
    else:
        return jsonify({'error': 'Failed to convert webpage to markdown'}), 400

if __name__ == '__main__':
    app.run(debug=True) 