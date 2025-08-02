# Setup Instructions

## 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click "New repository"
3. Repository name: `az104`
4. Description: `AZ-104 Azure Administrator Course Content Crawler & Vietnamese Translation Project`
5. Set to Public
6. Don't initialize with README (we already have one)
7. Click "Create repository"

## 2. Setup Git and Push Initial Code

```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/az104.git

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: AZ-104 course crawler with 260 units crawled"

# Push to main branch
git branch -M main
git push -u origin main
```

## 3. Install Git Flow

### macOS (using Homebrew)
```bash
brew install git-flow-avh
```

### Ubuntu/Debian
```bash
sudo apt-get install git-flow
```

### Windows
```bash
# Using Git Bash or WSL
curl -OL https://raw.github.com/nvie/gitflow/develop/contrib/gitflow-installer.sh
bash gitflow-installer.sh
```

## 4. Initialize Git Flow

```bash
# Initialize git flow (use default settings)
git flow init

# This will create:
# - main branch (production)
# - develop branch (integration)
```

## 5. Git Flow Commands Reference

### Feature Development
```bash
# Start a new feature
git flow feature start translation-engine

# Work on your feature...
git add .
git commit -m "Add translation engine"

# Finish feature (merges to develop)
git flow feature finish translation-engine
```

### Release Process
```bash
# Start a release
git flow release start v1.0.0

# Prepare release (update version, docs, etc.)
git add .
git commit -m "Prepare release v1.0.0"

# Finish release (merges to main and develop, creates tag)
git flow release finish v1.0.0
```

### Hotfix Process
```bash
# Start a hotfix
git flow hotfix start critical-bug-fix

# Fix the bug...
git add .
git commit -m "Fix critical bug"

# Finish hotfix (merges to main and develop)
git flow hotfix finish critical-bug-fix
```

## 6. Push All Branches

```bash
# Push develop branch
git checkout develop
git push -u origin develop

# Push main branch
git checkout main
git push origin main
```