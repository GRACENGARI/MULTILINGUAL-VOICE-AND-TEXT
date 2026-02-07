# 📤 GitHub Setup Guide

Complete guide to push your African Language AI Tutor to GitHub.

## 🎯 Prerequisites

1. **Git installed** on your computer
   - Windows: Download from [git-scm.com](https://git-scm.com/download/win)
   - Mac: `brew install git` or download from git-scm.com
   - Linux: `sudo apt install git` or `sudo yum install git`

2. **GitHub account**
   - Create one at [github.com](https://github.com/signup)

3. **GitHub repository created**
   - Go to [github.com/new](https://github.com/new)
   - Name it: `african-language-tutor`
   - Keep it public or private
   - **Don't** initialize with README (we already have one)

## 🚀 Method 1: Automated Script (Recommended)

### For Windows:
```cmd
push_to_github.bat
```

### For Linux/Mac:
```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

The script will:
1. Initialize Git repository
2. Add all files
3. Create initial commit
4. Ask for your GitHub repository URL
5. Push to GitHub

## 🔧 Method 2: Manual Steps

### Step 1: Initialize Git Repository
```bash
git init
```

### Step 2: Add Files
```bash
git add .
```

### Step 3: Create Initial Commit
```bash
git commit -m "Initial commit: African Language AI Tutor with RAG architecture"
```

### Step 4: Add GitHub Remote
Replace `yourusername` with your GitHub username:
```bash
git remote add origin https://github.com/yourusername/african-language-tutor.git
```

### Step 5: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

## 🔐 Authentication

### Option 1: Personal Access Token (Recommended)
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (full control)
4. Copy the token
5. Use it as password when pushing

### Option 2: SSH Key
1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. Add to GitHub: Settings → SSH and GPG keys
3. Use SSH URL: `git@github.com:yourusername/african-language-tutor.git`

## 📝 After Pushing

### 1. Update Repository Settings
- Add description: "AI-powered language tutor for African languages using RAG"
- Add topics: `ai`, `language-learning`, `african-languages`, `rag`, `gemini`, `streamlit`
- Add website: Your deployed URL (if any)

### 2. Create README.md
```bash
# Rename the GitHub README
mv README_GITHUB.md README.md
git add README.md
git commit -m "Update README for GitHub"
git push
```

### 3. Add License
Create a `LICENSE` file with MIT License:
```bash
# Copy MIT License template from GitHub
# Or use: https://choosealicense.com/licenses/mit/
```

### 4. Add Contributing Guidelines
Create `CONTRIBUTING.md`:
```markdown
# Contributing to African Language AI Tutor

We welcome contributions! Please see our guidelines...
```

## 🎨 Enhance Your Repository

### Add Badges
Add these to your README.md:
```markdown
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
```

### Add Screenshots
1. Take screenshots of your app
2. Create `screenshots/` folder
3. Add images to README

### Add Demo Video
1. Record a demo video
2. Upload to YouTube
3. Add link to README

## 🚨 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/yourusername/african-language-tutor.git
```

### Error: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --allow-unrelated-histories
git push origin main
```

### Error: "Permission denied"
- Check your GitHub credentials
- Use Personal Access Token instead of password
- Or set up SSH key

### Error: "Repository not found"
- Make sure you created the repository on GitHub
- Check the repository URL is correct
- Verify you have access to the repository

## 📦 What Gets Pushed

### ✅ Included:
- All Python files
- Language knowledge bases (JSON)
- Documentation (MD files)
- Requirements.txt
- Setup scripts
- .gitignore

### ❌ Excluded (via .gitignore):
- .env file (contains API key)
- __pycache__/
- Virtual environment
- Generated audio files
- FAISS index files

## 🔄 Future Updates

### To push updates:
```bash
git add .
git commit -m "Description of changes"
git push
```

### To create a new branch:
```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

### To create a release:
1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Add release notes
5. Publish release

## 🌟 Make It Popular

### 1. Share on Social Media
- Twitter/X with hashtags: #AI #LanguageLearning #AfricanLanguages
- LinkedIn with project description
- Reddit: r/MachineLearning, r/LanguageLearning

### 2. Submit to Lists
- Awesome lists on GitHub
- Product Hunt
- Hacker News

### 3. Write Blog Post
- Medium article about the project
- Dev.to tutorial
- Personal blog

### 4. Create Documentation Site
- Use GitHub Pages
- Or deploy to Vercel/Netlify

## 📊 Track Progress

### GitHub Insights
- Watch stars and forks
- Monitor issues and PRs
- Check traffic analytics

### Engagement
- Respond to issues quickly
- Welcome contributors
- Update regularly

## 🎉 Success Checklist

- [ ] Repository created on GitHub
- [ ] Code pushed successfully
- [ ] README.md updated
- [ ] .gitignore configured
- [ ] License added
- [ ] Topics/tags added
- [ ] Description added
- [ ] Screenshots added
- [ ] Contributing guidelines added
- [ ] First release created

---

**Need help?** Open an issue on GitHub or check the documentation!

**Ready to share your project with the world!** 🌍✨