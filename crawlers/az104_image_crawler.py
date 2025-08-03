#!/usr/bin/env python3
"""
AZ-104 Enhanced Crawler with Image Support
Production-ready crawler for Microsoft Learn content with image downloading
"""

import asyncio
import json
import re
import time
import aiohttp
import hashlib
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import aiofiles
from urllib.parse import urljoin, urlparse

class AZ104ImageCrawler:
    """Enhanced crawler with image support for AZ-104 course content"""
    
    def __init__(self):
        self.base_url = "https://learn.microsoft.com"
        self.output_dir = Path("content")
        self.assets_dir = self.output_dir / "assets"
        
        # Create directories
        (self.output_dir / "english").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "vietnamese").mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Image download session
        self.session = None
        self.downloaded_images = {}  # Cache to avoid re-downloading
        
    async def init_session(self):
        """Initialize HTTP session for image downloads"""
        if not self.session or self.session.closed:
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=30,
                ttl_dns_cache=300,
                use_dns_cache=True,
            )
            timeout = aiohttp.ClientTimeout(total=60, connect=30)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def clean_filename(self, filename):
        """Clean filename for filesystem compatibility"""
        filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
        filename = re.sub(r'\s+', '_', filename)
        return filename[:100]
    
    async def get_actual_image_urls(self, page):
        """Get actual image URLs from the page using Playwright"""
        try:
            # Wait with timeout and retry
            for attempt in range(2):
                try:
                    await page.wait_for_load_state('networkidle', timeout=30000)
                    break
                except Exception as e:
                    if attempt == 1:
                        print(f"⚠️  Load state timeout, continuing anyway...")
                        break
                    await asyncio.sleep(2)
            
            image_elements = await page.query_selector_all('img')
            image_urls = {}
            
            for img_element in image_elements:
                try:
                    src = await img_element.get_attribute('src')
                    if src and not src.startswith('data:'):
                        actual_url = await page.evaluate('(img) => img.src', img_element)
                        image_urls[src] = actual_url if actual_url != src else src
                except:
                    continue
            
            return image_urls
        except Exception as e:
            print(f"⚠️  Error getting actual image URLs: {e}")
            return {}

    async def download_image_direct(self, img_url):
        """Download image directly using the actual URL"""
        try:
            await self.init_session()
            
            if img_url in self.downloaded_images:
                return self.downloaded_images[img_url]
            
            if img_url.startswith('data:'):
                return img_url
            
            parsed_url = urlparse(img_url)
            original_name = Path(parsed_url.path).name or "image"
            
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            file_ext = Path(original_name).suffix or '.png'
            local_filename = f"{Path(original_name).stem}_{url_hash}{file_ext}"
            local_path = self.assets_dir / local_filename
            
            # Skip if already exists
            if local_path.exists():
                relative_path = f"../../../assets/{local_filename}"
                self.downloaded_images[img_url] = relative_path
                return relative_path
            
            print(f"📷 Downloading image: {img_url}")
            
            # Retry logic for image download
            for attempt in range(3):
                try:
                    async with self.session.get(img_url, timeout=30) as response:
                        if response.status == 200:
                            content = await response.read()
                            async with aiofiles.open(local_path, 'wb') as f:
                                await f.write(content)
                            
                            relative_path = f"../../../assets/{local_filename}"
                            self.downloaded_images[img_url] = relative_path
                            print(f"✅ Downloaded: {local_filename}")
                            return relative_path
                        else:
                            print(f"❌ Failed to download {img_url}: HTTP {response.status}")
                            return img_url
                except Exception as e:
                    if attempt == 2:
                        print(f"❌ Error downloading {img_url} after 3 attempts: {e}")
                        return img_url
                    print(f"⚠️  Download attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(2)
                    
        except Exception as e:
            print(f"❌ Error downloading {img_url}: {e}")
            return img_url

    async def process_images_with_actual_urls(self, soup, actual_image_urls):
        """Process and download all images using actual URLs from the page"""
        images = soup.find_all('img')
        if not images:
            print("📷 No images found in content")
            return soup
        
        print(f"📷 Processing {len(images)} images...")
        
        for img in images:
            src = img.get('src')
            if not src:
                continue
            
            actual_url = actual_image_urls.get(src, src)
            local_path = await self.download_image_direct(actual_url)
            img['src'] = local_path
            
            if not img.get('alt'):
                img['alt'] = "Course content image"
            
            img['loading'] = 'lazy'
        
        return soup

    async def extract_content_with_images(self, page, unit_url, unit_title):
        """Extract content including images from a unit page"""
        print(f"📖 Extracting: {unit_title}")
        
        try:
            # Increase timeout and add retry logic
            for attempt in range(3):
                try:
                    await page.goto(unit_url, wait_until='networkidle', timeout=60000)
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    print(f"⚠️  Attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(5)
            
            await page.wait_for_timeout(5000)  # Increased wait time
            
            page_title = await page.title()
            actual_image_urls = await self.get_actual_image_urls(page)
            print(f"🔍 Found {len(actual_image_urls)} images with actual URLs")
            
            main_content = await page.query_selector('#module-unit-content')
            if not main_content:
                main_content = await page.query_selector('main')
                if not main_content:
                    main_content = await page.query_selector('[data-bi-name="content"]')
            
            if main_content:
                content_html = await main_content.inner_html()
                soup = BeautifulSoup(content_html, 'html.parser')
                
                # Remove unwanted elements
                unwanted_selectors = [
                    '.xp-tag', '.metadata', '.page-metadata',
                    '[data-progress-uid]', '[data-bi-name="feedback"]',
                    '.visually-hidden', '.docon', 
                    'button', '.button', '[role="button"]',
                    '.feedback', '.rating', '.helpful',
                    '.navigation', '.breadcrumb',
                    '.next-unit', '.prev-unit'
                ]
                
                for selector in unwanted_selectors:
                    for element in soup.select(selector):
                        element.decompose()
                
                soup = await self.process_images_with_actual_urls(soup, actual_image_urls)
                clean_html = self._create_clean_html_with_css(page_title, unit_title, unit_url, soup)
                return clean_html
            else:
                print(f"⚠️  No main content found for {unit_url}")
                return self._create_error_html(unit_url, "No main content found")
            
        except Exception as e:
            print(f"❌ Error extracting content from {unit_url}: {e}")
            return self._create_error_html(unit_url, str(e))

    def _create_clean_html_with_css(self, page_title, unit_title, unit_url, content_soup):
        """Create clean HTML with embedded CSS and proper image styling"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 30px 20px;
            color: #333;
            background-color: #fff;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #0078d4;
            margin-top: 2em;
            margin-bottom: 1em;
            font-weight: 600;
        }}
        
        h1 {{ 
            border-bottom: 3px solid #0078d4; 
            padding-bottom: 15px; 
            font-size: 2.2em;
            margin-bottom: 1.5em;
        }}
        
        h2 {{ 
            font-size: 1.6em; 
            border-left: 4px solid #0078d4;
            padding-left: 15px;
        }}
        
        h3 {{ font-size: 1.3em; }}
        h4 {{ font-size: 1.1em; }}
        
        p {{
            margin: 16px 0;
            text-align: justify;
            line-height: 1.7;
        }}
        
        ul, ol {{
            margin: 20px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 10px 0;
            line-height: 1.6;
        }}
        
        code {{
            background-color: #f6f8fa;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
            color: #d73a49;
        }}
        
        pre {{
            background-color: #f6f8fa;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 4px solid #0078d4;
            margin: 20px 0;
        }}
        
        pre code {{
            background: none;
            padding: 0;
            color: #333;
        }}
        
        blockquote {{
            border-left: 4px solid #0078d4;
            padding: 20px;
            margin: 20px 0;
            background-color: #f8f9fa;
            border-radius: 4px;
            font-style: italic;
        }}
        
        .source-info {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 5px solid #2196f3;
            font-size: 0.9em;
        }}
        
        .source-info h2 {{
            margin-top: 0;
            color: #1976d2;
            font-size: 1.2em;
        }}
        
        .translation-placeholder {{
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            padding: 20px;
            border-radius: 8px;
            margin-top: 40px;
            border-left: 5px solid #ff9800;
        }}
        
        .translation-placeholder h2 {{
            margin-top: 0;
            color: #f57c00;
            font-size: 1.2em;
        }}
        
        img {{ 
            max-width: 100%; 
            height: auto; 
            margin: 25px 0;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: block;
            margin-left: auto;
            margin-right: auto;
        }}
        
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin: 25px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 15px; 
            text-align: left; 
        }}
        
        th {{ 
            background-color: #f5f5f5; 
            font-weight: bold;
            color: #0078d4;
        }}
        
        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }}
        
        strong {{
            color: #0078d4;
            font-weight: 600;
        }}
        
        a {{
            color: #0078d4;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .alert {{
            padding: 15px;
            margin: 20px 0;
            border-radius: 6px;
            border-left: 4px solid;
        }}
        
        .alert.is-info {{
            background-color: #e3f2fd;
            border-left-color: #2196f3;
            color: #1976d2;
        }}
        
        .alert.is-warning {{
            background-color: #fff3e0;
            border-left-color: #ff9800;
            color: #f57c00;
        }}
        
        .alert-title {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="source-info">
        <h2>📚 Course Information</h2>
        <p><strong>Unit:</strong> {unit_title}</p>
        <p><strong>Source:</strong> <a href="{unit_url}" target="_blank">{unit_url}</a></p>
        <p><strong>Course:</strong> AZ-104: Microsoft Azure Administrator</p>
    </div>
    
    <div class="main-content">
        {content_soup.prettify()}
    </div>
    
    <div class="translation-placeholder">
        <h2>🇻🇳 Vietnamese Translation</h2>
        <p><em>Bản dịch tiếng Việt sẽ được thêm vào đây...</em></p>
        <p><em>Translation will be added here...</em></p>
    </div>
</body>
</html>"""
    
    def _create_error_html(self, url, error):
        """Create error HTML"""
        return f"""<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
    <h1>Error Extracting Content</h1>
    <p>Could not extract content from: <a href="{url}">{url}</a></p>
    <p>Error: {error}</p>
</body>
</html>"""
    
    async def recrawl_single_unit(self, unit_url, output_path):
        """Re-crawl a single unit with image support"""
        print(f"🔄 Re-crawling unit: {unit_url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            page = await browser.new_page()
            
            # Set longer timeouts
            page.set_default_timeout(90000)
            page.set_default_navigation_timeout(90000)
            
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            try:
                unit_title = unit_url.split('/')[-2].replace('-', ' ').title()
                content = await self.extract_content_with_images(page, unit_url, unit_title)
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
                    await f.write(content)
                
                print(f"✅ Successfully re-crawled: {output_path.name}")
                return True
                
            except Exception as e:
                print(f"❌ Error re-crawling {unit_url}: {e}")
                return False
            finally:
                await browser.close()
                # Don't close session here, let batch processor handle it

async def main():
    """Test the enhanced crawler with a specific unit"""
    crawler = AZ104ImageCrawler()
    
    test_url = "https://learn.microsoft.com/en-us/training/modules/tour-azure-portal/2-azure-management/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az104-admin-prerequisites"
    output_path = Path("content/english/01_AZ-104-_Prerequisites_for_Azure_administrators/01_Tour_Azure_Portal/02_Azure_management_options.html")
    
    success = await crawler.recrawl_single_unit(test_url, output_path)
    
    if success:
        print("🎉 Test crawl completed successfully!")
        print(f"📁 Check the updated file: {output_path}")
        print(f"🖼️  Images saved to: {crawler.assets_dir}")
    else:
        print("❌ Test crawl failed")

if __name__ == "__main__":
    asyncio.run(main())