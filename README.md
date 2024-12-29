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



#### Using Docker Compose (Recommended)
1. Make sure you have Docker and Docker Compose installed
2. Create `.env` file with your API keys
3. Run:
   ```bash
   docker compose up
   ```
   - Use `-d` flag to run in background: `docker compose up -d`
   - To rebuild: `docker compose up --build`
   - To stop: `docker compose down`


Access the application at `http://localhost:5001`

## Project Structure

```
.
├── app.py                  # Main Flask application
├── dev_server.py          # Development server with hot reloading
├── website_to_markdown.py # Firecrawl API integration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose configuration
└── templates/
    └── index.html        # Frontend interface
```