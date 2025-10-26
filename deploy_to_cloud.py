#!/usr/bin/env python3
"""
One-Click Cloud Deployment Script
Deploy your AI Schedule Creator to a permanent cloud URL
"""

import subprocess
import webbrowser
import time
import os

def check_git_status():
    """Check if Git repository is ready for deployment"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            print("📝 You have uncommitted changes:")
            print(result.stdout)
            return False
        return True
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first.")
        return False

def commit_and_push():
    """Commit and push changes to GitHub"""
    try:
        print("📦 Committing changes...")
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy interactive AI Schedule Creator'], check=True)
        
        print("🚀 Pushing to GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Successfully pushed to GitHub!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

def deploy_to_railway():
    """Deploy to Railway.app"""
    print("\n🚀 Deploying to Railway.app...")
    print("=" * 50)
    
    print("1. Go to: https://railway.app")
    print("2. Sign up/Login with GitHub")
    print("3. Click 'Deploy from GitHub repo'")
    print("4. Select your calendar-scheduler repository")
    print("5. Railway will automatically deploy!")
    print("6. Get your permanent URL!")
    
    webbrowser.open('https://railway.app')
    
    print("\n💡 Your app will be available 24/7 at:")
    print("   https://your-app-name.railway.app")

def deploy_to_render():
    """Deploy to Render.com"""
    print("\n🚀 Deploying to Render.com...")
    print("=" * 50)
    
    print("1. Go to: https://render.com")
    print("2. Sign up/Login with GitHub")
    print("3. Click 'New Web Service'")
    print("4. Connect your calendar-scheduler repository")
    print("5. Render will use render.yaml automatically")
    print("6. Get your permanent URL!")
    
    webbrowser.open('https://render.com')
    
    print("\n💡 Your app will be available 24/7 at:")
    print("   https://your-app-name.onrender.com")

def main():
    """Main deployment function"""
    print("🌐 AI Schedule Creator - Cloud Deployment")
    print("=" * 60)
    print("This will create a permanent URL that doesn't need your local machine!")
    print()
    
    # Check Git status
    if not check_git_status():
        print("\n⚠️  Please commit your changes first:")
        print("   git add .")
        print("   git commit -m 'Your message'")
        print("   git push origin main")
        return
    
    # Commit and push
    if not commit_and_push():
        return
    
    print("\n🎯 Choose your deployment platform:")
    print("1. Railway.app (Recommended - Easy setup)")
    print("2. Render.com (Alternative)")
    print("3. Both (Deploy to multiple platforms)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        deploy_to_railway()
    elif choice == "2":
        deploy_to_render()
    elif choice == "3":
        deploy_to_railway()
        print("\n" + "="*50)
        deploy_to_render()
    else:
        print("❌ Invalid choice. Please run the script again.")
        return
    
    print("\n🎉 Deployment instructions completed!")
    print("💡 Your AI Schedule Creator will be permanently available!")
    print("🔄 No more need to keep your local machine running!")

if __name__ == '__main__':
    main()
