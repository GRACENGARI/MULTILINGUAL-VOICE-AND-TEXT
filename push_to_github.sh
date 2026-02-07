#!/bin/bash
# Script to push African Language Tutor to GitHub (Linux/Mac)

echo "========================================"
echo "African Language AI Tutor - GitHub Push"
echo "========================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo "Please install Git first."
    exit 1
fi

echo ""
echo "Step 1: Initializing Git repository..."
if [ ! -d .git ]; then
    git init
    echo "Git repository initialized!"
else
    echo "Git repository already exists."
fi

echo ""
echo "Step 2: Adding files to Git..."
git add .
echo "Files added!"

echo ""
echo "Step 3: Creating initial commit..."
git commit -m "Initial commit: African Language AI Tutor with RAG architecture"
echo "Commit created!"

echo ""
echo "Step 4: Setting up GitHub remote..."
echo ""
echo "Please enter your GitHub repository URL"
echo "Example: https://github.com/yourusername/african-language-tutor.git"
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "ERROR: No repository URL provided!"
    exit 1
fi

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    git remote set-url origin "$REPO_URL"
    echo "Remote updated!"
else
    git remote add origin "$REPO_URL"
    echo "Remote added!"
fi

echo ""
echo "Step 5: Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Push failed!"
    echo ""
    echo "Possible solutions:"
    echo "1. Make sure you created the repository on GitHub"
    echo "2. Check your GitHub credentials"
    echo "3. Try: git push -u origin main --force"
    exit 1
fi

echo ""
echo "========================================"
echo "SUCCESS! Project pushed to GitHub!"
echo "========================================"
echo ""
echo "Your repository: $REPO_URL"
echo ""
echo "Next steps:"
echo "1. Visit your GitHub repository"
echo "2. Add a description and topics"
echo "3. Enable GitHub Pages (optional)"
echo "4. Share with the community!"
echo ""