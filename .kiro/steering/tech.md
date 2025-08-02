# Technical Stack & Build System

## Dependencies
- **Python**: 3.8+ required
- **Web Scraping**: requests, beautifulsoup4, lxml
- **Browser Automation**: playwright (with Chromium browser)
- **File Operations**: aiofiles, pathlib
- **Data Processing**: json, re (built-in)

## Installation & Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Automated setup (recommended)
python setup_and_run.py
```

## Common Commands

### Running Crawlers
```bash
# Main advanced crawler (recommended)
python az104_advanced_crawler.py

# Alternative crawler versions
python az104_complete_crawler.py
python az104_final_crawler_fixed.py

# Test crawler functionality
python test_crawler.py
```

### Content Processing
```bash
# Clean up crawled HTML content
python cleanup_content.py

# Advanced content cleanup
python advanced_cleanup.py
```

### Project Setup
```bash
# Complete setup and run
python setup_and_run.py
```

## Code Patterns

### Filename Sanitization
- Use `clean_filename()` method for filesystem-safe names
- Replace invalid characters with hyphens or underscores
- Limit filename length to 100 characters

### Web Scraping Best Practices
- Implement exponential backoff retry logic
- Add delays between requests (1-2 seconds)
- Use proper User-Agent headers
- Handle HTTP errors gracefully

### Content Structure
- Preserve Microsoft's hierarchical organization
- Extract main content areas using BeautifulSoup selectors
- Remove navigation, ads, and UI elements
- Maintain source URL metadata in each file

## File Formats
- **Input**: Web pages from Microsoft Learn
- **Output**: Clean HTML files with embedded CSS
- **Metadata**: JSON structure files for course organization
- **Reports**: Markdown summary files