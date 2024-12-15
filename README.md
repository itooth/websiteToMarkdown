# Website to Markdown Converter

A web application that converts web pages to Markdown format with AI-powered cleaning and formatting.

## Features

- Convert any webpage to Markdown format using Firecrawl API
- AI-powered cleaning and formatting of Markdown content
- Side-by-side comparison of original and cleaned Markdown
- History management with:
  - Drag-and-drop reordering
  - Multiple selection and combining
  - Delete functionality
  - Browser-based storage (localStorage)
- Copy to clipboard functionality
- Real-time preview

## Setup

### Local Development

1. Install dependencies:
   ```bash
   pip install flask python-dotenv requests markdown2 livereload
   ```

2. Set up environment variables in `.env`:
   ```
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   CHATANYWHERE_API_KEY=your_chatanywhere_api_key
   ```

3. Run development server:
   ```bash
   python dev_server.py
   ```

### Docker Setup

1. Pull and run the Docker image:
   ```bash
   docker run -p 5001:5001 \
     -e FIRECRAWL_API_KEY=your_firecrawl_api_key \
     -e CHATANYWHERE_API_KEY=your_chatanywhere_api_key \
     kim0809/websitetomarkdown
   ```

2. Access the application at `http://localhost:5001`

#### Data Persistence in Docker

By default, the history data is stored in the browser's localStorage, which means:
- Data persists across browser sessions
- Data is tied to the browser, not the container
- Data is not shared between different browsers or devices
- Data survives container restarts as it's stored client-side

For persistent server-side storage, you have several options:

1. **Using Docker Volume for File-based Storage**:
   ```bash
   # Create a volume
   docker volume create markdown-history

   # Run container with volume
   docker run -p 5001:5001 \
     -v markdown-history:/app/data \
     -e FIRECRAWL_API_KEY=your_key \
     -e CHATANYWHERE_API_KEY=your_key \
     kim0809/websitetomarkdown
   ```

2. **Using External Database**:
   - Set up a MongoDB or SQLite database
   - Mount the database file as a volume
   - Configure database connection in environment variables

3. **Using Host Directory**:
   ```bash
   # Mount a host directory
   docker run -p 5001:5001 \
     -v /path/to/host/data:/app/data \
     -e FIRECRAWL_API_KEY=your_key \
     -e CHATANYWHERE_API_KEY=your_key \
     kim0809/websitetomarkdown
   ```

### Building Docker Image Locally

1. Clone the repository
2. Build the image:
   ```bash
   docker build -t kim0809/websitetomarkdown .
   ```
3. Run the container:
   ```bash
   docker run -p 5001:5001 \
     -e FIRECRAWL_API_KEY=your_firecrawl_api_key \
     -e CHATANYWHERE_API_KEY=your_chatanywhere_api_key \
     kim0809/websitetomarkdown
   ```

## Code Structure

```
.
├── app.py                  # Main Flask application
├── dev_server.py           # Development server with hot reloading
├── website_to_markdown.py  # Firecrawl API integration
├── .env                    # Environment variables (not in repo)
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── .dockerignore         # Files to exclude from Docker build
└── templates/
    └── index.html        # Frontend interface
```

### Code Documentation

#### Dockerfile
```dockerfile
FROM python:3.9-slim          # Base image with Python 3.9
WORKDIR /app                  # Set working directory
COPY requirements.txt .       # Copy dependencies file
RUN pip install --no-cache-dir -r requirements.txt  # Install dependencies
COPY . .                     # Copy application code
EXPOSE 5001                  # Expose application port
CMD ["python", "app.py"]     # Start the application
```

#### Key Components

1. **Backend (app.py)**
   - Flask web server with hot reloading
   - Integration with Firecrawl API for webpage conversion
   - Integration with ChatAnywhere API for AI cleaning
   - Environment variable management

2. **Frontend (templates/index.html)**
   - History Management using localStorage
   - Multiple Selection and Combining functionality
   - Real-time Markdown preview
   - Drag-and-drop reordering using Sortable.js

3. **Development Server (dev_server.py)**
   - Implements hot reloading for development
   - Watches for file changes
   - Automatically restarts server when needed

4. **API Integration (website_to_markdown.py)**
   - Handles Firecrawl API requests
   - Processes webpage to Markdown conversion
   - Manages API authentication and error handling

## Development

- Use `dev_server.py` for hot reloading during development
- Frontend changes will reload automatically
- Backend changes will restart the server

## API Integration

1. **Firecrawl API**
   - Used for converting webpages to Markdown
   - Requires API key in environment variables
   - Handles various webpage formats

2. **ChatAnywhere API**
   - Used for AI-powered Markdown cleaning
   - Formats and structures content
   - Removes irrelevant parts

## Troubleshooting

### Firecrawl API Issues

1. **400 Bad Request - Unrecognized Keys**
   - Problem: API rejects requests with extra configuration options
   - Solution: Keep the request body minimal with only required fields:
     ```json
     {
       "url": "https://example.com",
       "formats": ["markdown"]
     }
     ```

2. **Partial Content from Dynamic Websites**
   - Problem: Some websites may return incomplete content
   - Solutions:
     - Try using the `/v1/crawl` endpoint
     - Consider using the actions feature
     - Contact Firecrawl support for guidance

3. **Timeout Issues**
   - Problem: API requests timing out for complex pages
   - Solutions:
     - Increase request timeout
     - Break down large pages
     - Use batch processing

### Docker Issues

1. **Container Not Starting**
   - Check if environment variables are properly set
   - Verify port 5001 is not in use
   - Check Docker logs: `docker logs <container_id>`

2. **API Connection Issues**
   - Verify API keys are correctly passed to container
   - Check network connectivity
   - Ensure API endpoints are accessible

3. **Performance Issues**
   - Container resource limits can be adjusted:
     ```bash
     docker run -p 5001:5001 \
       --memory=1g \
       --cpus=1 \
       -e FIRECRAWL_API_KEY=your_key \
       -e CHATANYWHERE_API_KEY=your_key \
       kim0809/websitetomarkdown
     ```

4. **Data Persistence Issues**
   - History data is stored in browser's localStorage by default
   - To persist data across devices or share between users:
     - Use Docker volumes for file-based storage
     - Set up an external database
     - Mount a host directory
   - Clear browser cache/localStorage if history becomes corrupted