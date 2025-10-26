#!/bin/bash
# GitHub Repository Setup Script

echo "🚀 Setting up GitHub repository for AI Schedule Creator..."
echo ""

# Get repository URL from user
echo "📝 Please provide your GitHub repository URL:"
echo "   Example: https://github.com/yourusername/calendar-scheduler.git"
echo ""
read -p "Enter your GitHub repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No URL provided. Please run the script again."
    exit 1
fi

echo ""
echo "🔗 Connecting to GitHub repository..."

# Add remote origin
git remote add origin "$REPO_URL"

# Push to GitHub
echo "📤 Pushing code to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Your repository is now available at: ${REPO_URL%.git}"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Go to https://railway.app"
    echo "2. Sign up with GitHub"
    echo "3. Click 'Deploy from GitHub repo'"
    echo "4. Select your calendar-scheduler repository"
    echo "5. Railway will automatically deploy!"
    echo ""
    echo "💡 Your permanent URL will be: https://your-app-name.railway.app"
else
    echo "❌ Failed to push to GitHub. Please check your repository URL and try again."
fi
