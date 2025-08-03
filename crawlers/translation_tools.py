#!/usr/bin/env python3
"""
Translation tools for AZ-104 Vietnamese content
"""

import asyncio
import json
from pathlib import Path
from bs4 import BeautifulSoup
import aiofiles

class TranslationTools:
    """Tools for managing Vietnamese translations"""
    
    def __init__(self):
        self.english_dir = Path("content/english")
        self.vietnamese_dir = Path("content/vietnamese")
        self.vietnamese_dir.mkdir(exist_ok=True)
        self.processed_count = 0
        
    async def create_vietnamese_template(self, english_file_path):
        """Create Vietnamese template from English HTML file"""
        try:
            async with aiofiles.open(english_file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Update title
            title_tag = soup.find('title')
            if title_tag:
                title_tag.string = title_tag.string + " - Tiếng Việt"
            
            # Update translation placeholder
            translation_div = soup.find('div', class_='translation-placeholder')
            if translation_div:
                translation_div.clear()
                
                vietnamese_header = soup.new_tag('h2')
                vietnamese_header.string = "🇻🇳 Nội dung tiếng Việt"
                translation_div.append(vietnamese_header)
                
                main_content = soup.find('div', class_='main-content')
                if main_content:
                    vietnamese_content = soup.new_tag('div', **{'class': 'vietnamese-content'})
                    
                    english_content = main_content.find('div', id='module-unit-content')
                    if english_content:
                        vietnamese_unit_content = soup.new_tag('div', id='vietnamese-unit-content')
                        
                        instruction_p = soup.new_tag('p')
                        instruction_p['style'] = 'font-style: italic; color: #666; border: 1px dashed #ccc; padding: 15px; background: #f9f9f9;'
                        instruction_p.string = "📝 Nội dung dịch tiếng Việt sẽ được thêm vào đây. Vui lòng dịch từng phần một cách chính xác và giữ nguyên định dạng HTML."
                        vietnamese_unit_content.append(instruction_p)
                        
                        vietnamese_content.append(vietnamese_unit_content)
                    
                    translation_div.append(vietnamese_content)
            
            # Save Vietnamese template
            relative_path = english_file_path.relative_to(self.english_dir)
            vietnamese_file_path = self.vietnamese_dir / relative_path
            vietnamese_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(vietnamese_file_path, 'w', encoding='utf-8') as f:
                await f.write(str(soup))
            
            self.processed_count += 1
            print(f"✅ Created template: {relative_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating template for {english_file_path}: {e}")
            return False
    
    async def create_all_templates(self):
        """Create Vietnamese templates for all English content"""
        print("🔄 Creating Vietnamese translation templates...")
        print("=" * 60)
        
        english_files = list(self.english_dir.rglob("*.html"))
        print(f"📁 Found {len(english_files)} English files to process")
        
        batch_size = 20
        for i in range(0, len(english_files), batch_size):
            batch = english_files[i:i + batch_size]
            tasks = [self.create_vietnamese_template(file_path) for file_path in batch]
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
            if i + batch_size < len(english_files):
                await asyncio.sleep(1)
        
        print(f"\n🎉 Template creation completed!")
        print(f"✅ Successfully created: {self.processed_count} templates")
        print(f"📁 Templates saved to: {self.vietnamese_dir}")
        
        await self.create_structure_summary()
    
    async def create_structure_summary(self):
        """Create a summary of the Vietnamese content structure"""
        structure = {
            "project": "AZ-104 Vietnamese Translation",
            "created_templates": self.processed_count,
            "structure": {}
        }
        
        for learning_path_dir in sorted(self.vietnamese_dir.iterdir()):
            if learning_path_dir.is_dir():
                path_name = learning_path_dir.name
                structure["structure"][path_name] = {"modules": {}}
                
                for module_dir in sorted(learning_path_dir.iterdir()):
                    if module_dir.is_dir():
                        module_name = module_dir.name
                        html_files = list(module_dir.glob("*.html"))
                        structure["structure"][path_name]["modules"][module_name] = {
                            "unit_count": len(html_files),
                            "units": [f.name for f in sorted(html_files)]
                        }
        
        summary_file = self.vietnamese_dir / "translation_structure.json"
        async with aiofiles.open(summary_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(structure, indent=2, ensure_ascii=False))
        
        print(f"📊 Structure summary saved to: {summary_file}")

    async def create_terminology_database(self):
        """Create a terminology database for consistent translations"""
        terminology = {
            "azure_services": {
                "Azure Active Directory": "Azure Active Directory",
                "Microsoft Entra ID": "Microsoft Entra ID",
                "Virtual Machine": "Máy ảo",
                "Storage Account": "Tài khoản lưu trữ",
                "Resource Group": "Nhóm tài nguyên",
                "Subscription": "Đăng ký",
                "Virtual Network": "Mạng ảo"
            },
            "general_tech": {
                "Authentication": "Xác thực",
                "Authorization": "Ủy quyền",
                "Backup": "Sao lưu",
                "Restore": "Khôi phục",
                "Scale": "Mở rộng quy mô",
                "Monitor": "Giám sát",
                "Alert": "Cảnh báo"
            },
            "ui_elements": {
                "Dashboard": "Bảng điều khiển",
                "Portal": "Cổng thông tin",
                "Blade": "Blade",
                "Settings": "Cài đặt",
                "Properties": "Thuộc tính"
            }
        }
        
        terminology_file = Path("content/terminology/az104_vietnamese_terms.json")
        terminology_file.parent.mkdir(exist_ok=True)
        
        async with aiofiles.open(terminology_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(terminology, indent=2, ensure_ascii=False))
        
        print(f"📚 Terminology database created: {terminology_file}")

async def main():
    """Main function for translation tools"""
    tools = TranslationTools()
    
    print("AZ-104 Translation Tools")
    print("=" * 30)
    print("1. Create Vietnamese templates")
    print("2. Create terminology database")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        await tools.create_all_templates()
    elif choice == "2":
        await tools.create_terminology_database()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid option selected.")

if __name__ == "__main__":
    asyncio.run(main())