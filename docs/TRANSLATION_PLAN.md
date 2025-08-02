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
- [x] Git Flow implementation
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

## 🔄 Git Flow Translation Workflow

### 1. Start Translation Feature
```bash
# Start translating a learning path
git flow feature start translate-path-01-prerequisites

# Or start translating a specific module
git flow feature start translate-identity-management
```

### 2. Translation Process
```bash
# Work on translation files
# Edit files in content/vietnamese/ directory

# Commit progress regularly
git add content/vietnamese/01_Prerequisites/
git commit -m "Translate Prerequisites Path: Modules 1-2 completed"

# Push feature branch for backup/collaboration
git push origin feature/translate-path-01-prerequisites
```

### 3. Complete Translation Feature
```bash
# Finish the feature (merges to develop)
git flow feature finish translate-path-01-prerequisites

# Push updated develop branch
git push origin develop
```

## 📝 Translation Guidelines

### Technical Terminology
- **Azure**: Giữ nguyên "Azure"
- **Resource Group**: "Nhóm tài nguyên"
- **Virtual Machine**: "Máy ảo"
- **Storage Account**: "Tài khoản lưu trữ"
- **Virtual Network**: "Mạng ảo"
- **Subscription**: "Gói đăng ký"

### Content Structure
1. **Keep HTML structure intact**
2. **Translate content in placeholder sections**
3. **Preserve code examples** (translate comments only)
4. **Maintain Microsoft Learn links**
5. **Keep technical accuracy**

### File Organization
```
content/vietnamese/
├── 01_Prerequisites/
│   ├── 01_Tour_Azure_Portal/
│   │   ├── 01_Introduction.html
│   │   └── ...
│   └── ...
└── ...
```

## 🛠️ Translation Tools & Scripts

### Create Translation Template
```bash
# Copy English structure to Vietnamese
python scripts/create_translation_template.py
```

### Validate Translation
```bash
# Check translation completeness
python scripts/validate_translation.py
```

### Generate Progress Report
```bash
# Generate translation progress report
python scripts/translation_progress.py
```

## 📋 Translation Checklist

### Per Unit Translation
- [ ] Copy English file to Vietnamese directory
- [ ] Translate title and headings
- [ ] Translate paragraph content
- [ ] Translate list items
- [ ] Review code examples (translate comments)
- [ ] Check links and references
- [ ] Proofread for accuracy
- [ ] Test HTML rendering

### Per Module Review
- [ ] Consistency check across units
- [ ] Technical terminology verification
- [ ] Cross-references validation
- [ ] Module summary translation

### Per Learning Path Review
- [ ] Path overview translation
- [ ] Learning objectives translation
- [ ] Prerequisites translation
- [ ] Summary and next steps

## 🎯 Quality Standards

### Language Quality
- **Clarity**: Easy to understand for Vietnamese learners
- **Accuracy**: Technically correct translations
- **Consistency**: Uniform terminology usage
- **Naturalness**: Sounds natural in Vietnamese

### Technical Quality
- **HTML Validity**: Proper HTML structure
- **Link Integrity**: All links work correctly
- **Code Preservation**: Code examples remain functional
- **Format Consistency**: Consistent styling and layout

## 📈 Progress Tracking

### Weekly Milestones
- **Week 1-2**: Setup and planning
- **Week 3-4**: Learning Path 1 (Prerequisites)
- **Week 5-6**: Learning Path 2 (Identity & Governance)
- **Week 7-8**: Learning Path 3 (Virtual Networks)
- **Week 9-10**: Learning Path 4 (Storage)
- **Week 11-12**: Learning Path 5 (Compute Resources)
- **Week 13**: Learning Path 6 (Monitoring & Backup)
- **Week 14**: Final review and quality assurance

### Success Metrics
- **Completion Rate**: % of units translated
- **Quality Score**: Review feedback rating
- **Consistency Score**: Terminology usage consistency
- **Technical Accuracy**: Technical review pass rate

## 🤝 Collaboration Guidelines

### Branch Naming
- `feature/translate-path-NN-name`
- `feature/translate-module-name`
- `feature/review-path-NN`
- `hotfix/fix-translation-issue`

### Commit Messages
- `Translate: [Path/Module] - [Description]`
- `Review: [Path/Module] - [Changes]`
- `Fix: [Issue description]`

### Pull Request Process
1. Create feature branch
2. Complete translation work
3. Self-review and test
4. Create pull request to develop
5. Peer review (if applicable)
6. Merge to develop
7. Regular releases to main

## 📞 Support & Resources

### Reference Materials
- [Microsoft Azure Documentation](https://docs.microsoft.com/azure/)
- [Azure Terminology Glossary](https://docs.microsoft.com/azure/azure-glossary-cloud-terminology)
- [Vietnamese IT Terminology](https://vi.wikipedia.org/wiki/Thuật_ngữ_công_nghệ_thông_tin)

### Tools
- HTML editors with Vietnamese support
- Translation memory tools
- Git Flow extensions
- Markdown editors

---

**Target Completion**: 14 weeks from project start
**Quality Goal**: Professional-grade Vietnamese translation suitable for certification study