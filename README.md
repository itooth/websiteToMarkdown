# Website to Markdown Converter

A web application that converts web pages to Markdown format with AI-powered cleaning and formatting.

## Features

- Convert webpages to Markdown using Firecrawl API
- AI-powered content cleaning and formatting
- Side-by-side comparison of original and cleaned Markdown
- History management with drag-and-drop reordering
- Copy to clipboard and real-time preview

## Setup

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   CHATANYWHERE_API_KEY=your_chatanywhere_api_key
   ```

3. Run the application:
   ```bash
   python app.py
   ```

For development with hot reloading:
```bash
python dev_server.py
```

### Docker Setup

Run with Docker:
```bash
docker run -p 5001:5001 \
  -e FIRECRAWL_API_KEY=your_firecrawl_api_key \
  -e CHATANYWHERE_API_KEY=your_chatanywhere_api_key \
  kim0809/websitetomarkdown
```

Access at `http://localhost:5001`

## Project Structure

```
.
├── app.py                  # Main Flask application
├── dev_server.py          # Development server with hot reloading
├── website_to_markdown.py # Firecrawl API integration
├── requirements.txt       # Python dependencies
└── templates/
    └── index.html        # Frontend interface
```