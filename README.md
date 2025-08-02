# AZ-104 Course Content Crawler & Translation Project

## 📚 Overview
This project crawls Microsoft Learn's AZ-104 Azure Administrator certification course content and prepares it for Vietnamese translation. It extracts structured learning materials from Microsoft's online training platform while preserving the original format and organization.

## 🎯 Purpose
- **Content Extraction**: Systematically crawl all AZ-104 course materials from Microsoft Learn
- **Translation Preparation**: Structure content for Vietnamese localization with built-in translation placeholders
- **Content Preservation**: Maintain Microsoft's original course structure and formatting
- **Offline Access**: Enable offline study and translation work

## ✨ Key Features
- Hierarchical content organization (Learning Path → Module → Unit)
- Respectful web crawling with rate limiting and retry logic
- HTML content cleaning and standardization
- Bilingual content structure with translation placeholders
- Comprehensive course structure metadata in JSON format

## 📊 Current Status
Successfully crawled **260 units** across **31 modules** in **6 learning paths**, covering the complete AZ-104 certification curriculum.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for Playwright)

### Installation
```bash
# Install dependencies
python setup_and_run.py

# Or manually:
pip install -r requirements.txt
playwright install chromium
```

### Usage

#### Crawl Course Content
```bash
python az104_complete_crawler.py
```

#### Clean Existing Content
```bash
python advanced_cleanup.py
```

## 📁 Project Structure
```
az104/
├── az104_course_content/
│   ├── english_original/     # Crawled English content
│   ├── vietnamese_translation/ # Vietnamese translations
│   ├── assets/              # Images and resources
│   ├── course_structure.json # Course metadata
│   └── CRAWL_SUMMARY.md     # Crawl statistics
├── *.py                     # Crawler and utility scripts
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🌐 Course Structure

### Learning Paths (6)
1. **Prerequisites for Azure administrators** (5 modules, 38 units)
2. **Manage identities and governance in Azure** (6 modules, 53 units)
3. **Configure and manage virtual networks** (8 modules, 60 units)
4. **Implement and manage storage in Azure** (4 modules, 39 units)
5. **Deploy and manage Azure compute resources** (5 modules, 48 units)
6. **Monitor and back up Azure resources** (3 modules, 22 units)

## 🛠️ Available Scripts

- `az104_complete_crawler.py` - Main crawler for all course content
- `advanced_cleanup.py` - Advanced content cleaning and formatting
- `setup_and_run.py` - Automated setup and installation
- `test_crawler.py` - Test crawler functionality

## 🇻🇳 Translation Guidelines

### Translation Process
1. **Content Review**: Review English content in `content/english/`
2. **Translation**: Add Vietnamese content to placeholder sections
3. **Quality Check**: Ensure technical accuracy and readability
4. **Structure Preservation**: Maintain original HTML structure and formatting

### Translation Standards
- **Technical Terms**: Use established Vietnamese Azure terminology
- **Code Examples**: Keep code in English, translate comments
- **UI Elements**: Translate interface elements consistently
- **Links**: Preserve original Microsoft Learn links

## 🤝 Contributing

1. Review the existing content structure
2. Follow the established naming conventions
3. Test any changes thoroughly
4. Maintain the original Microsoft Learn formatting

## 📄 License

This project is for educational purposes. All original content belongs to Microsoft Corporation.

## 🔗 Links

- [Microsoft Learn AZ-104](https://learn.microsoft.com/en-us/training/courses/az-104t00)
- [Azure Administrator Certification](https://learn.microsoft.com/en-us/credentials/certifications/azure-administrator/)

---

**Note**: This project respects Microsoft's terms of service and is intended for educational and translation purposes only.