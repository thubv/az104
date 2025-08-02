#!/usr/bin/env python3
"""
Setup script for AZ-104 crawler
Installs dependencies and sets up the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "content/english",
        "content/vietnamese", 
        "content/assets",
        "docs",
        "scripts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def create_css_file():
    """Create the main CSS file"""
    css_content = """/* AZ-104 Course Content Styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 30px 20px;
    color: #333;
    background-color: #fff;
}

h1, h2, h3, h4, h5, h6 {
    color: #0078d4;
    margin-top: 2em;
    margin-bottom: 1em;
    font-weight: 600;
}

h1 { 
    border-bottom: 3px solid #0078d4; 
    padding-bottom: 15px; 
    font-size: 2.2em;
    margin-bottom: 1.5em;
}

h2 { 
    font-size: 1.6em; 
    border-left: 4px solid #0078d4;
    padding-left: 15px;
}

h3 { font-size: 1.3em; }
h4 { font-size: 1.1em; }

p {
    margin: 16px 0;
    text-align: justify;
    line-height: 1.7;
}

ul, ol {
    margin: 20px 0;
    padding-left: 30px;
}

li {
    margin: 10px 0;
    line-height: 1.6;
}

code {
    background-color: #f6f8fa;
    padding: 3px 8px;
    border-radius: 4px;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.9em;
    color: #d73a49;
}

pre {
    background-color: #f6f8fa;
    padding: 20px;
    border-radius: 8px;
    overflow-x: auto;
    border-left: 4px solid #0078d4;
    margin: 20px 0;
}

pre code {
    background: none;
    padding: 0;
    color: #333;
}

blockquote {
    border-left: 4px solid #0078d4;
    padding: 20px;
    margin: 20px 0;
    background-color: #f8f9fa;
    border-radius: 4px;
    font-style: italic;
}

.source-info {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 30px;
    border-left: 5px solid #2196f3;
    font-size: 0.9em;
}

.source-info h2 {
    margin-top: 0;
    color: #1976d2;
    font-size: 1.2em;
}

.translation-placeholder {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    padding: 20px;
    border-radius: 8px;
    margin-top: 40px;
    border-left: 5px solid #ff9800;
}

.translation-placeholder h2 {
    margin-top: 0;
    color: #f57c00;
    font-size: 1.2em;
}

img { 
    max-width: 100%; 
    height: auto; 
    margin: 25px 0;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

table { 
    border-collapse: collapse; 
    width: 100%; 
    margin: 25px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

th, td { 
    border: 1px solid #ddd; 
    padding: 15px; 
    text-align: left; 
}

th { 
    background-color: #f5f5f5; 
    font-weight: bold;
    color: #0078d4;
}

.highlight {
    background-color: #fff3cd;
    padding: 15px;
    border-radius: 6px;
    border-left: 4px solid #ffc107;
    margin: 20px 0;
}

strong {
    color: #0078d4;
    font-weight: 600;
}

a {
    color: #0078d4;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}"""
    
    css_file = Path("content/assets/styles.css")
    css_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"🎨 Created CSS file: {css_file}")

def main():
    print("🚀 Setting up AZ-104 Course Crawler")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Create directories
    create_directories()
    
    # Create CSS file
    create_css_file()
    
    # Install requirements
    if not run_command("pip install playwright beautifulsoup4 aiofiles requests lxml", "Installing Python packages"):
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Install Playwright browsers
    if not run_command("playwright install chromium", "Installing Playwright browser"):
        print("❌ Failed to install Playwright browser")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the crawler:")
    print("python scripts/az104_crawler.py")
    print("\nTo clean content:")
    print("python scripts/content_cleaner.py")

if __name__ == "__main__":
    main()