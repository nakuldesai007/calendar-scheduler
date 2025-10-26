#!/usr/bin/env python3
"""
One-Click Deployment to Railway.app
Creates a permanent public URL for your Schedule Creator
"""

import subprocess
import webbrowser
import time

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Railway CLI not found")
    return False

def install_railway_cli():
    """Install Railway CLI"""
    print("🔧 Installing Railway CLI...")
    
    try:
        # Try npm first
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        print("✅ Railway CLI installed via npm")
        return True
    except subprocess.CalledProcessError:
        try:
            # Try brew
            subprocess.run(['brew', 'install', 'railway'], check=True)
            print("✅ Railway CLI installed via Homebrew")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Railway CLI")
            print("💡 Please install manually:")
            print("   1. Go to https://railway.app")
            print("   2. Sign up for free")
            print("   3. Install CLI: npm install -g @railway/cli")
            return False

def deploy_to_railway():
    """Deploy to Railway.app"""
    print("🚀 Deploying to Railway.app...")
    
    try:
        # Login to Railway
        print("🔐 Logging in to Railway...")
        subprocess.run(['railway', 'login'], check=True)
        
        # Initialize project
        print("📁 Initializing Railway project...")
        subprocess.run(['railway', 'init'], check=True)
        
        # Deploy
        print("🚀 Deploying...")
        result = subprocess.run(['railway', 'deploy'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            
            # Get the URL
            url_result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
            if url_result.returncode == 0:
                domain = url_result.stdout.strip()
                public_url = f"https://{domain}"
                print(f"🌐 Your Schedule Creator is live at: {public_url}")
                
                # Open in browser
                webbrowser.open(public_url)
                
                return public_url
            else:
                print("✅ Deployed successfully!")
                print("💡 Check your Railway dashboard for the URL")
                return True
        else:
            print("❌ Deployment failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Schedule Creator - One-Click Railway Deployment")
    print("=" * 60)
    
    # Check Railway CLI
    if not check_railway_cli():
        if not install_railway_cli():
            return
    
    # Deploy
    result = deploy_to_railway()
    
    if result:
        print("\n🎉 SUCCESS!")
        print("=" * 20)
        if isinstance(result, str):
            print(f"🌐 Public URL: {result}")
        print("📱 Your Schedule Creator is now live!")
        print("🌍 Accessible from anywhere in the world")
        print("🔄 Automatic deployments on Git push")
        print("\n💡 Next steps:")
        print("   1. Push to GitHub: git push origin main")
        print("   2. Railway will auto-deploy on every push")
        print("   3. Share your permanent URL!")
    else:
        print("❌ Deployment failed")
        print("💡 Try manual deployment:")
        print("   1. Go to https://railway.app")
        print("   2. Connect your GitHub repository")
        print("   3. Railway will auto-deploy!")

if __name__ == '__main__':
    main()
