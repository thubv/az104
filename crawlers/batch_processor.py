#!/usr/bin/env python3
"""
Batch processor for AZ-104 content with various utilities
"""

import asyncio
import json
from pathlib import Path
from az104_image_crawler import AZ104ImageCrawler

class BatchProcessor:
    """Batch processing utilities for AZ-104 content"""
    
    def __init__(self):
        self.crawler = AZ104ImageCrawler()
        self.course_structure_file = Path("content/course_structure.json")
        self.processed_count = 0
        self.failed_count = 0
        
    async def load_course_structure(self):
        """Load the existing course structure"""
        if not self.course_structure_file.exists():
            print("❌ Course structure file not found!")
            return None
        
        with open(self.course_structure_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def recrawl_all_units(self):
        """Re-crawl all units with image support"""
        print("🚀 Starting batch re-crawl with image support")
        print("=" * 60)
        
        course_structure = await self.load_course_structure()
        if not course_structure:
            return
        
        total_units = sum(
            len(module.get('units', []))
            for learning_path in course_structure.get('learning_paths', [])
            for module in learning_path.get('modules', [])
        )
        
        print(f"📊 Found {total_units} units to re-crawl")
        
        for lp_index, learning_path in enumerate(course_structure.get('learning_paths', []), 1):
            print(f"\n🎯 Processing Learning Path {lp_index}: {learning_path.get('title', 'Unknown')}")
            
            for module_index, module in enumerate(learning_path.get('modules', []), 1):
                print(f"\n📁 Module {module_index}: {module.get('title', 'Unknown')}")
                
                units = module.get('units', [])
                batch_size = 5
                
                for i in range(0, len(units), batch_size):
                    batch = units[i:i + batch_size]
                    tasks = []
                    
                    for unit in batch:
                        unit_url = unit.get('url')
                        local_file = unit.get('local_file')
                        
                        if unit_url and local_file:
                            output_path = Path("content") / local_file
                            tasks.append(self.recrawl_unit_safe(unit_url, output_path, unit.get('title', 'Unknown')))
                    
                    if tasks:
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for result in results:
                            if result is True:
                                self.processed_count += 1
                            else:
                                self.failed_count += 1
                        
                        print(f"📊 Progress: {self.processed_count} success, {self.failed_count} failed")
                        await asyncio.sleep(2)
        
        print(f"\n🎉 Batch re-crawl completed!")
        print(f"✅ Successfully processed: {self.processed_count} units")
        print(f"❌ Failed: {self.failed_count} units")
        print(f"📊 Total: {self.processed_count + self.failed_count} units")
        
        await self.crawler.close_session()
    
    async def recrawl_unit_safe(self, unit_url, output_path, unit_title):
        """Safely re-crawl a single unit with error handling"""
        try:
            print(f"🔄 Re-crawling: {unit_title}")
            return await self.crawler.recrawl_single_unit(unit_url, output_path)
        except Exception as e:
            print(f"❌ Error re-crawling {unit_title}: {e}")
            return False

    async def fix_source_urls(self):
        """Fix source URLs in existing HTML files"""
        print("🔧 Fixing source URLs in HTML files...")
        
        html_files = list(Path("content/english").rglob("*.html"))
        print(f"📁 Found {len(html_files)} HTML files to process")
        
        fixed_count = 0
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                source_info = soup.find('div', class_='source-info')
                if source_info:
                    paragraphs = source_info.find_all('p')
                    for p in paragraphs:
                        if p.get_text() and 'Source:' in p.get_text():
                            link = p.find('a')
                            if link and link.get('href'):
                                url = link.get('href')
                                link.string = url
                                
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(str(soup))
                                
                                fixed_count += 1
                                break
            except Exception as e:
                print(f"❌ Error fixing {file_path}: {e}")
        
        print(f"✅ Fixed {fixed_count} files")

async def main():
    """Main function for batch processing"""
    processor = BatchProcessor()
    
    print("AZ-104 Batch Processor")
    print("=" * 30)
    print("1. Re-crawl all units with images")
    print("2. Fix source URLs")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        print("\n⚠️  This will re-crawl ALL 260 units with image support.")
        print("⚠️  This process may take 30-60 minutes to complete.")
        confirm = input("\n🤔 Do you want to continue? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            await processor.recrawl_all_units()
        else:
            print("❌ Operation cancelled.")
    
    elif choice == "2":
        await processor.fix_source_urls()
    
    elif choice == "3":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid option selected.")

if __name__ == "__main__":
    asyncio.run(main())