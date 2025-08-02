#!/usr/bin/env python3
"""
Setup script for AZ-104 crawler
"""

import subprocess
import sys
import os

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

def main():
    print("🚀 Setting up AZ-104 Course Crawler")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("❌ Failed to install requirements. Please install manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Install Playwright browsers
    if not run_command("playwright install chromium", "Installing Playwright browser"):
        print("❌ Failed to install Playwright browser. Please install manually:")
        print("playwright install chromium")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the crawler:")
    print("python az104_advanced_crawler.py")
    
    # Ask if user wants to run now
    response = input("\nDo you want to start crawling now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        print("\n🕷️ Starting crawler...")
        os.system("python az104_advanced_crawler.py")

if __name__ == "__main__":
    main()