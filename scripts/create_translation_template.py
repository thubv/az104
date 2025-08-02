#!/usr/bin/env python3
"""
Create Vietnamese translation template by copying English structure
"""

import os
import shutil
from pathlib import Path
import re

class TranslationTemplateCreator:
    def __init__(self):
        self.english_dir = Path("content/english")
        self.vietnamese_dir = Path("content/vietnamese")
        
    def create_vietnamese_structure(self):
        """Create Vietnamese directory structure matching English"""
        print("🏗️  Creating Vietnamese translation structure...")
        
        if not self.english_dir.exists():
            print("❌ English content directory not found!")
            return False
        
        # Create Vietnamese directory
        self.vietnamese_dir.mkdir(exist_ok=True)
        
        # Copy directory structure
        for root, dirs, files in os.walk(self.english_dir):
            # Calculate relative path
            rel_path = Path(root).relative_to(self.english_dir)
            vietnamese_path = self.vietnamese_dir / rel_path
            
            # Create directory in Vietnamese structure
            vietnamese_path.mkdir(parents=True, exist_ok=True)
            
            # Copy HTML files with translation placeholders
            for file in files:
                if file.endswith('.html'):
                    english_file = Path(root) / file
                    vietnamese_file = vietnamese_path / file
                    
                    if not vietnamese_file.exists():
                        self.create_translation_file(english_file, vietnamese_file)
        
        print("✅ Vietnamese translation structure created!")
        return True
    
    def create_translation_file(self, english_file, vietnamese_file):
        """Create Vietnamese translation file from English template"""
        try:
            with open(english_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace CSS path to point to shared assets
            content = re.sub(
                r'href="[^"]*assets/styles\.css"',
                'href="../../../assets/styles.css"',
                content
            )
            
            # Update source info to indicate this is Vietnamese version
            content = re.sub(
                r'<p><strong>Course:</strong> AZ-104: Microsoft Azure Administrator</p>',
                '<p><strong>Course:</strong> AZ-104: Microsoft Azure Administrator (Vietnamese)</p>',
                content
            )
            
            # Replace translation placeholder with Vietnamese content placeholder
            vietnamese_placeholder = '''    <div class="translation-placeholder">
        <h2>🇻🇳 Vietnamese Translation</h2>
        <p><strong>Status:</strong> <span style="color: #ff9800;">Translation needed</span></p>
        <p><em>Nội dung tiếng Việt cần được dịch ở đây...</em></p>
        <hr>
        <h3>Translation Guidelines:</h3>
        <ul>
            <li>Translate all text content while preserving HTML structure</li>
            <li>Keep technical terms consistent with Azure Vietnamese documentation</li>
            <li>Preserve code examples (translate comments only)</li>
            <li>Maintain links to original Microsoft Learn resources</li>
        </ul>
    </div>'''
            
            content = re.sub(
                r'<div class="translation-placeholder">.*?</div>',
                vietnamese_placeholder,
                content,
                flags=re.DOTALL
            )
            
            # Save Vietnamese file
            with open(vietnamese_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"📄 Created: {vietnamese_file.relative_to(Path.cwd())}")
            
        except Exception as e:
            print(f"❌ Error creating {vietnamese_file}: {e}")
    
    def generate_progress_report(self):
        """Generate translation progress report"""
        print("\n📊 Generating translation progress report...")
        
        english_files = list(self.english_dir.rglob("*.html"))
        vietnamese_files = list(self.vietnamese_dir.rglob("*.html"))
        
        total_files = len(english_files)
        created_files = len(vietnamese_files)
        
        progress = (created_files / total_files * 100) if total_files > 0 else 0
        
        report = f"""# Translation Progress Report

## Overview
- **Total English Files**: {total_files}
- **Vietnamese Templates Created**: {created_files}
- **Progress**: {progress:.1f}%

## Status
- ✅ Template Structure: {'Complete' if created_files == total_files else 'In Progress'}
- 🔄 Content Translation: Not Started
- ⏳ Quality Review: Pending

## Next Steps
1. Begin translating content in Vietnamese files
2. Start with Learning Path 1 (Prerequisites)
3. Maintain HTML structure and formatting

Generated: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        report_file = Path("docs/TRANSLATION_PROGRESS.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📋 Progress report saved: {report_file}")
        print(f"📈 Translation templates: {progress:.1f}% complete")

def main():
    creator = TranslationTemplateCreator()
    
    if creator.create_vietnamese_structure():
        creator.generate_progress_report()
        
        print("\n🎉 Translation template creation completed!")
        print("\n📝 Next steps:")
        print("1. Review created Vietnamese files")
        print("2. Begin translating content systematically")
        print("3. Start with Learning Path 1 (Prerequisites)")
        print("4. Maintain HTML structure and formatting")

if __name__ == "__main__":
    main()