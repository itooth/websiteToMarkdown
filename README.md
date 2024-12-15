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
  - Persistent storage
- Copy to clipboard functionality
- Real-time preview

## Key Components

### Backend (app.py)

- Flask web server with hot reloading
- Integration with Firecrawl API for webpage conversion
- Integration with ChatAnywhere API for AI cleaning
- Environment variable management

### Frontend (templates/index.html)

Key functionalities:

1. **History Management**
   ```javascript
   // Initialize history from localStorage
   let history = JSON.parse(localStorage.getItem('conversionHistory') || '[]');
   ```
   - Stores up to 50 recent conversions
   - Persists data in localStorage
   - Supports drag-and-drop reordering using Sortable.js

2. **Multiple Selection and Combining**
   ```javascript
   function combineSelectedMarkdown() {
       const selectedItems = history.filter((item, index) => {
           const checkbox = document.querySelector(`input[data-id="${index}"]`);
           return checkbox && checkbox.checked;
       });
       // Combines markdown with separators
       const combinedMarkdown = selectedItems.map(item => item.markdown).join('\n\n---\n\n');
   }
   ```
   - Select multiple history items
   - Combine them with separators
   - Update both original and cleaned panels

3. **Markdown Cleaning Process**
   - Uses AI to clean and format markdown
   - Removes irrelevant content
   - Improves formatting and structure
   - Preserves important content

## Setup

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
   - Note: Additional options like `javascript`, `renderDelay`, or `scrapeOptions` are not supported in the `/v1/scrape` endpoint

2. **Partial Content from Dynamic Websites**
   - Problem: Some websites (like Yuque) may return incomplete content
   - Solutions:
     - Try using the `/v1/crawl` endpoint instead of `/v1/scrape`
     - Consider using the actions feature for interactive content
     - Contact Firecrawl support for site-specific guidance

3. **Timeout Issues**
   - Problem: API requests timing out for complex pages
   - Solutions:
     - Increase the request timeout (e.g., `timeout=60`)
     - Break down large pages into smaller sections
     - Use batch processing for multiple URLs

### Common Error Messages

```json
{
  "success": false,
  "error": "Bad Request",
  "details": [{
    "code": "unrecognized_keys",
    "message": "Unrecognized key in body -- please review the v1 API documentation"
  }]
}
```

- This usually means you're including unsupported parameters
- Refer to the [Firecrawl documentation](https://docs.firecrawl.dev) for the correct request format

## File Structure

```
.
├── app.py              # Main Flask application
├── dev_server.py       # Development server with hot reloading
├── website_to_markdown.py  # Firecrawl API integration
├── .env               # Environment variables
└── templates/
    └── index.html     # Frontend interface
```