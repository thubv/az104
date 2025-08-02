#!/usr/bin/env python3
"""
Content Cleaner for AZ-104 Course
Cleans up crawled content by removing unnecessary elements
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

class ContentCleaner:
    def __init__(self, content_dir="content/english"):
        self.content_dir = Path(content_dir)
        
        # Unwanted text patterns to remove
        self.unwanted_patterns = [
            r'Get started with Azure.*?Sign up\.',
            r'Choose the Azure account.*?Sign up\.',
            r'Pay as you go or try Azure free.*?Sign up\.',
            r'Module incomplete:.*?Previous Go back to finish',
            r'Need help\? See our troubleshooting guide.*?reporting an issue\.',
            r'Feedback\s*Was this page helpful\?\s*Yes\s*No',
            r'Was this page helpful\?\s*Yes\s*No',
            r'Sign in to save your progress',
            r'Complete the module to unlock',
            r'XP\s*\d+\s*minutes?',
            r'Completed\s*\d+\s*XP',
            r'Unit \d+ of \d+',
            r'Previous\s*Next',
            r'Continue\s*Next unit:',
            r'Ask Learn',
            r'Browse all courses',
            r'Start learning path',
            r'Add to collection',
            r'Share this page'
        ]
    
    def extract_clean_content(self, html_content):
        """Extract only the essential learning content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main content area
        main_content = soup.find('div', id='module-unit-content')
        if not main_content:
            main_content = soup.find('div', class_='content')
            if not main_content:
                main_content = soup.find('main')
        
        if main_content:
            # Remove unwanted elements
            unwanted_selectors = [
                '.xp-tag', '.metadata', '.page-metadata',
                '[data-progress-uid]', '[data-bi-name]',
                '.visually-hidden', '.docon', 
                'button', '.button', '[role="button"]',
                '.feedback', '.rating', '.helpful',
                '.navigation', '.breadcrumb', '.uhf-container',
                '[data-test-id]', '.site-header',
                '.module-progress', '.completion',
                '.cta', '.call-to-action', '.promo',
                '.ad', '.advertisement'
            ]
            
            for selector in unwanted_selectors:
                for element in main_content.select(selector):
                    element.decompose()
            
            # Remove text nodes matching unwanted patterns
            for text_node in main_content.find_all(string=True):
                text = text_node.strip()
                for pattern in self.unwanted_patterns:
                    if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                        parent = text_node.parent
                        if parent:
                            parent.decompose()
                        break
            
            # Clean up empty elements
            for element in main_content.find_all():
                if not element.get_text(strip=True) and not element.find('img') and element.name not in ['br', 'hr']:
                    element.decompose()
            
            return main_content
        
        return None
    
    def clean_file(self, file_path):
        """Clean a single HTML file"""
        print(f"🧹 Cleaning: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1) if title_match else "Content"
            
            source_match = re.search(r'<strong>Source:</strong>.*?<a href="([^"]*)"', content)
            source_url = source_match.group(1) if source_match else ""
            
            unit_match = re.search(r'<strong>Unit:</strong>\s*([^<]*)', content)
            unit_title = unit_match.group(1) if unit_match else ""
            
            # Extract clean content
            clean_content = self.extract_clean_content(content)
            
            if clean_content:
                # Create clean HTML with external CSS
                clean_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../../../assets/styles.css">
</head>
<body>
    <div class="source-info">
        <h2>📚 Course Information</h2>
        <p><strong>Unit:</strong> {unit_title}</p>
        <p><strong>Source:</strong> <a href="{source_url}" target="_blank">Microsoft Learn</a></p>
        <p><strong>Course:</strong> AZ-104: Microsoft Azure Administrator</p>
    </div>
    
    <div class="main-content">
        {clean_content.prettify()}
    </div>
    
    <div class="translation-placeholder">
        <h2>🇻🇳 Vietnamese Translation</h2>
        <p><em>Bản dịch tiếng Việt sẽ được thêm vào đây...</em></p>
    </div>
</body>
</html>"""
                
                # Save cleaned content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(clean_html)
                
                return True
            else:
                print(f"⚠️  Could not find main content in {file_path.name}")
                return False
                
        except Exception as e:
            print(f"❌ Error cleaning {file_path}: {e}")
            return False
    
    def clean_all_files(self):
        """Clean all HTML files"""
        print("🚀 Starting content cleanup...")
        print("=" * 50)
        
        total_files = 0
        cleaned_files = 0
        
        for root, dirs, files in os.walk(self.content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = Path(root) / file
                    total_files += 1
                    
                    if self.clean_file(file_path):
                        cleaned_files += 1
        
        print("=" * 50)
        print(f"🎉 Cleanup completed!")
        print(f"📊 Total files: {total_files}")
        print(f"✅ Successfully cleaned: {cleaned_files}")
        print(f"❌ Failed: {total_files - cleaned_files}")

def main():
    cleaner = ContentCleaner()
    cleaner.clean_all_files()

if __name__ == "__main__":
    main()