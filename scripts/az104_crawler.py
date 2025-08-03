#!/usr/bin/env python3
"""
AZ-104 Microsoft Learn Course Crawler
Main script to crawl the complete AZ-104 course content
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

class AZ104Crawler:
    def __init__(self):
        self.base_url = "https://learn.microsoft.com"
        self.course_url = "https://learn.microsoft.com/en-us/training/courses/az-104t00"
        self.output_dir = Path("content")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create directories
        (self.output_dir / "english").mkdir(exist_ok=True)
        (self.output_dir / "vietnamese").mkdir(exist_ok=True)
        (self.output_dir / "assets").mkdir(exist_ok=True)
        
        # All 6 learning paths
        self.learning_paths = [
            {
                'title': 'AZ-104: Prerequisites for Azure administrators',
                'url': '/en-us/training/paths/az-104-administrator-prerequisites/',
                'expected_modules': 5
            },
            {
                'title': 'AZ-104: Manage identities and governance in Azure',
                'url': '/en-us/training/paths/az-104-manage-identities-governance/',
                'expected_modules': 6
            },
            {
                'title': 'AZ-104: Configure and manage virtual networks for Azure administrators',
                'url': '/en-us/training/paths/az-104-manage-virtual-networks/',
                'expected_modules': 8
            },
            {
                'title': 'AZ-104: Implement and manage storage in Azure',
                'url': '/en-us/training/paths/az-104-manage-storage/',
                'expected_modules': 4
            },
            {
                'title': 'AZ-104: Deploy and manage Azure compute resources',
                'url': '/en-us/training/paths/az-104-manage-compute-resources/',
                'expected_modules': 5
            },
            {
                'title': 'AZ-104: Monitor and back up Azure resources',
                'url': '/en-us/training/paths/az-104-monitor-backup-resources/',
                'expected_modules': 3
            }
        ]
    
    def clean_filename(self, filename):
        """Clean filename for filesystem compatibility"""
        filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
        filename = re.sub(r'\s+', '_', filename)
        return filename[:100]
    
    async def save_content(self, content, filepath):
        """Save content to file asynchronously"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(content)
        print(f"✅ Saved: {filepath.name}")
    
    def group_units_by_module(self, units):
        """Group units by their module (based on URL pattern)"""
        modules = {}
        
        for unit in units:
            url_parts = unit['url'].split('/')
            if 'modules' in url_parts:
                module_idx = url_parts.index('modules')
                if module_idx + 1 < len(url_parts):
                    module_name = url_parts[module_idx + 1]
                    
                    if module_name not in modules:
                        modules[module_name] = {
                            'name': module_name,
                            'title': module_name.replace('-', ' ').title(),
                            'units': []
                        }
                    
                    modules[module_name]['units'].append(unit)
        
        return list(modules.values())
    
    async def extract_units_from_learning_path(self, page, path_url):
        """Extract all units from a learning path"""
        print(f"🔍 Extracting units from: {path_url}")
        
        full_url = self.base_url + path_url
        await page.goto(full_url)
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(2000)
        
        unit_links = await page.query_selector_all('a[href*="/training/modules/"]')
        
        units = []
        seen_urls = set()
        
        for link in unit_links:
            try:
                href = await link.get_attribute('href')
                if not href or href in seen_urls:
                    continue
                
                seen_urls.add(href)
                
                if href.startswith('/'):
                    full_unit_url = self.base_url + href
                else:
                    full_unit_url = href
                
                title = await link.inner_text()
                title = title.strip()
                
                if title and full_unit_url and title.lower() != 'start':
                    units.append({
                        'title': title,
                        'url': full_unit_url
                    })
                    
            except Exception as e:
                continue
        
        print(f"📚 Found {len(units)} units in this learning path")
        return units
    
    async def download_image(self, session, img_url, assets_dir):
        """Download image and return local path"""
        try:
            # Create a hash-based filename to avoid conflicts
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            parsed_url = urlparse(img_url)
            file_ext = Path(parsed_url.path).suffix or '.jpg'
            local_filename = f"img_{url_hash}{file_ext}"
            local_path = assets_dir / local_filename
            
            # Skip if already downloaded
            if local_path.exists():
                return f"../../../assets/{local_filename}"
            
            async with session.get(img_url) as response:
                if response.status == 200:
                    content = await response.read()
                    async with aiofiles.open(local_path, 'wb') as f:
                        await f.write(content)
                    print(f"📷 Downloaded image: {local_filename}")
                    return f"../../../assets/{local_filename}"
                else:
                    print(f"❌ Failed to download image: {img_url} (Status: {response.status})")
                    return img_url
        except Exception as e:
            print(f"❌ Error downloading image {img_url}: {e}")
            return img_url

    async def process_images(self, soup, base_url, assets_dir):
        """Process and download images in the content"""
        images = soup.find_all('img')
        if not images:
            return soup
        
        print(f"🖼️  Processing {len(images)} images...")
        
        async with aiohttp.ClientSession() as session:
            for img in images:
                src = img.get('src')
                if not src:
                    continue
                
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    img_url = 'https:' + src
                elif src.startswith('/'):
                    img_url = urljoin(base_url, src)
                elif not src.startswith('http'):
                    img_url = urljoin(base_url, src)
                else:
                    img_url = src
                
                # Download and update src
                local_path = await self.download_image(session, img_url, assets_dir)
                img['src'] = local_path
                
                # Add alt text if missing
                if not img.get('alt'):
                    img['alt'] = "Course content image"
        
        return soup

    async def extract_clean_content(self, page, unit_url, unit_title):
        """Extract and clean content from a unit page"""
        print(f"📖 Extracting: {unit_title}")
        
        try:
            await page.goto(unit_url)
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(1000)
            
            page_title = await page.title()
            
            # Find main content
            main_content = await page.query_selector('#module-unit-content')
            if not main_content:
                main_content = await page.query_selector('main')
            
            if main_content:
                content_html = await main_content.inner_html()
                soup = BeautifulSoup(content_html, 'html.parser')
                
                # Remove unwanted elements
                unwanted_selectors = [
                    '.xp-tag', '.metadata', '.page-metadata',
                    '[data-progress-uid]', '[data-bi-name]',
                    '.visually-hidden', '.docon', 
                    'button', '.button', '[role="button"]',
                    '.feedback', '.rating', '.helpful',
                    '.navigation', '.breadcrumb'
                ]
                
                for selector in unwanted_selectors:
                    for element in soup.select(selector):
                        element.decompose()
                
                # Process images
                assets_dir = self.output_dir / "assets"
                soup = await self.process_images(soup, self.base_url, assets_dir)
                
                # Create clean HTML
                clean_html = self._create_clean_html(page_title, unit_title, unit_url, soup)
                return clean_html
            
        except Exception as e:
            print(f"❌ Error extracting content from {unit_url}: {e}")
            return self._create_error_html(unit_url, str(e))
    
    def _create_clean_html(self, page_title, unit_title, unit_url, content_soup):
        """Create clean HTML with consistent styling"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="stylesheet" href="../../../assets/styles.css">
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
    
    async def crawl_learning_path(self, page, path_info, path_index):
        """Crawl a single learning path"""
        print(f"\n🎯 Processing Learning Path {path_index}: {path_info['title']}")
        
        path_dir = self.output_dir / "english" / f"{path_index:02d}_{self.clean_filename(path_info['title'])}"
        
        units = await self.extract_units_from_learning_path(page, path_info['url'])
        modules = self.group_units_by_module(units)
        
        print(f"📦 Organized into {len(modules)} modules")
        
        path_structure = {
            'title': path_info['title'],
            'url': self.base_url + path_info['url'],
            'expected_modules': path_info['expected_modules'],
            'actual_modules': len(modules),
            'modules': []
        }
        
        for module_index, module in enumerate(modules, 1):
            print(f"\n📁 Module {module_index}: {module['title']}")
            
            module_dir = path_dir / f"{module_index:02d}_{self.clean_filename(module['title'])}"
            
            module_structure = {
                'title': module['title'],
                'units': []
            }
            
            for unit_index, unit in enumerate(module['units'], 1):
                try:
                    content = await self.extract_clean_content(page, unit['url'], unit['title'])
                    
                    unit_filename = f"{unit_index:02d}_{self.clean_filename(unit['title'])}.html"
                    unit_filepath = module_dir / unit_filename
                    await self.save_content(content, unit_filepath)
                    
                    module_structure['units'].append({
                        'title': unit['title'],
                        'url': unit['url'],
                        'local_file': str(unit_filepath.relative_to(self.output_dir))
                    })
                    
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"❌ Error processing unit {unit['title']}: {e}")
                    continue
            
            path_structure['modules'].append(module_structure)
            await asyncio.sleep(2)
        
        return path_structure
    
    async def crawl_complete_course(self):
        """Crawl the complete AZ-104 course"""
        print("🚀 Starting AZ-104 Course Crawl")
        print("=" * 60)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            course_structure = {
                'course_title': 'AZ-104: Microsoft Azure Administrator',
                'course_url': self.course_url,
                'crawl_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_learning_paths': len(self.learning_paths),
                'learning_paths': []
            }
            
            try:
                for path_index, path_info in enumerate(self.learning_paths, 1):
                    try:
                        print(f"\n{'='*20} LEARNING PATH {path_index}/{len(self.learning_paths)} {'='*20}")
                        path_structure = await self.crawl_learning_path(page, path_info, path_index)
                        course_structure['learning_paths'].append(path_structure)
                        
                        print(f"⏳ Waiting 10 seconds before next learning path...")
                        await asyncio.sleep(10)
                        
                    except Exception as e:
                        print(f"❌ Error processing learning path {path_info['title']}: {e}")
                        continue
                
            finally:
                await browser.close()
            
            # Save course structure
            structure_file = self.output_dir / "course_structure.json"
            async with aiofiles.open(structure_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(course_structure, indent=2, ensure_ascii=False))
            
            print(f"\n🎉 Course crawl completed!")
            print(f"📊 Structure saved to: {structure_file}")
            print(f"📁 Content saved to: {self.output_dir}")
            
            return course_structure

async def main():
    crawler = AZ104Crawler()
    await crawler.crawl_complete_course()

if __name__ == "__main__":
    asyncio.run(main())