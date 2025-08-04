# AZ-104 Vietnamese Translation Plan

## 📊 Translation Overview

### Current Status
- **Total Units**: 260
- **Total Modules**: 31  
- **Total Learning Paths**: 6
- **English Content**: ✅ Complete (100%)
- **Vietnamese Translation**: 🔄 In Progress (0%)

## 🎯 Translation Strategy

### Phase 1: Foundation Setup (Week 1-2)
- [x] Content crawling and cleaning
- [x] Project structure setup
- [x] Content cleanup and formatting
- [ ] Translation workflow establishment
- [ ] Terminology glossary creation

### Phase 2: Core Translation (Week 3-12)
- [ ] Learning Path 1: Prerequisites (38 units)
- [ ] Learning Path 2: Identity & Governance (53 units)
- [ ] Learning Path 3: Virtual Networks (60 units)
- [ ] Learning Path 4: Storage (39 units)
- [ ] Learning Path 5: Compute Resources (48 units)
- [ ] Learning Path 6: Monitoring & Backup (22 units)

### Phase 3: Quality Assurance (Week 13-14)
- [ ] Technical review
- [ ] Language consistency check
- [ ] Final proofreading

## 🔄 Translation Workflow

### 1. Setup Translation Structure
```bash
# Create Vietnamese file templates
python scripts/create_translation_template.py
```

### 2. Translation Process
- Edit files in `az104_course_content/vietnamese_translation/` directory
- Maintain HTML structure and formatting
- Replace English content with Vietnamese translations
- Preserve all links and technical references

### 3. Quality Control
- Review technical accuracy
- Ensure consistent terminology
- Test all links and formatting

## 📝 Translation Guidelines

### Technical Terminology
- **Azure**: Giữ nguyên "Azure"
- **Resource Group**: "Resource Group"
- **Virtual Machine**: "Virtual Machine"
- **Storage Account**: "Storage Account"
- **Virtual Network**: "Virtual Network"
- **Subscription**: "Subscription"

### Content Structure
1. **Keep HTML structure intact**
2. **Translate content in placeholder sections**
3. **Preserve code examples** (translate comments only)
4. **Maintain Microsoft Learn links**
5. **Keep technical accuracy**w