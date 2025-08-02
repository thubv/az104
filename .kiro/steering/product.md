# AZ-104 Course Content Crawler & Translation Project

## Overview
This project crawls Microsoft Learn's AZ-104 Azure Administrator certification course content and prepares it for Vietnamese translation. It extracts structured learning materials from Microsoft's online training platform while preserving the original format and organization.

## Purpose
- **Content Extraction**: Systematically crawl all AZ-104 course materials from Microsoft Learn
- **Translation Preparation**: Structure content for Vietnamese localization with built-in translation placeholders
- **Content Preservation**: Maintain Microsoft's original course structure and formatting
- **Offline Access**: Enable offline study and translation work

## Key Features
- Hierarchical content organization (Learning Path → Module → Unit)
- Respectful web crawling with rate limiting and retry logic
- HTML content cleaning and standardization
- Bilingual content structure with translation placeholders
- Comprehensive course structure metadata in JSON format

## Current Status
Successfully crawled **260 units** across **31 modules** in **6 learning paths**, covering the complete AZ-104 certification curriculum.