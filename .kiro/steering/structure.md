# Project Structure & Organization

## Root Directory Layout
```
├── az104_course_content/           # Main content directory
│   ├── english_original/           # Crawled English content
│   ├── vietnamese_translation/     # Vietnamese translations (empty)
│   ├── assets/                     # Images and resources
│   ├── course_structure.json       # Complete course metadata
│   └── CRAWL_SUMMARY.md           # Crawl report and statistics
├── scripts/                        # Utility scripts
├── test_output/                    # Test results and temporary files
├── requirements.txt                # Python dependencies
└── *.py                           # Crawler and processing scripts
```

## Content Hierarchy
The course content follows Microsoft Learn's structure:
```
Learning Path (6 total)
├── Module (31 total)
    └── Unit (260 total)
```

### Learning Paths
1. **01_AZ-104-_Prerequisites_for_Azure_administrators** (5 modules, 38 units)
2. **02_AZ-104-_Manage_identities_and_governance_in_Azure** (6 modules, 53 units)
3. **03_AZ-104-_Configure_and_manage_virtual_networks** (8 modules, 60 units)
4. **04_AZ-104-_Implement_and_manage_storage_in_Azure** (4 modules, 39 units)
5. **05_AZ-104-_Deploy_and_manage_Azure_compute_resources** (5 modules, 48 units)
6. **06_AZ-104-_Monitor_and_back_up_Azure_resources** (3 modules, 22 units)

## File Naming Conventions
- **Directories**: `NN_Descriptive_Name_With_Underscores`
- **HTML Files**: `NN_Unit_Title_With_Underscores.html`
- **Numbers**: Zero-padded (01, 02, etc.) for proper sorting
- **Characters**: Invalid filesystem characters replaced with hyphens/underscores
- **Length**: Limited to 100 characters maximum

## Script Categories

### Crawler Scripts
- `az104_advanced_crawler.py` - Main production crawler
- `az104_complete_crawler.py` - Alternative implementation
- `az104_final_crawler_fixed.py` - Bug-fixed version
- `az104_crawler.py` - Basic crawler implementation

### Processing Scripts
- `cleanup_content.py` - HTML content cleaning
- `advanced_cleanup.py` - Enhanced content processing
- `setup_and_run.py` - Automated project setup

### Utility Scripts
- `test_crawler.py` - Testing functionality
- `scripts/` directory - Additional utilities

## Content File Structure
Each HTML file contains:
- **Source metadata**: Original URL and extraction timestamp
- **Clean content**: Processed HTML with embedded CSS
- **Translation placeholder**: Vietnamese translation section
- **Styling**: Consistent CSS for readability

## Key Files
- `course_structure.json` - Complete course metadata and file mappings
- `CRAWL_SUMMARY.md` - Detailed crawl statistics and progress report
- `requirements.txt` - Python package dependencies