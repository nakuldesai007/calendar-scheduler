#!/usr/bin/env python3
"""
Public URL Generator using ngrok
Creates a public URL for your Schedule Creator application
"""

import subprocess
import requests
import time
import webbrowser
import os

def install_ngrok():
    """Install ngrok if not already installed"""
    print("🔧 Installing ngrok...")
    
    # Check if ngrok is already installed
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok is already installed")
            return True
    except FileNotFoundError:
        pass
    
    # Install ngrok using Homebrew (macOS)
    try:
        subprocess.run(['brew', 'install', 'ngrok/ngrok/ngrok'], check=True)
        print("✅ ngrok installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install ngrok via Homebrew")
        print("💡 Please install ngrok manually:")
        print("   1. Go to https://ngrok.com/")
        print("   2. Sign up for a free account")
        print("   3. Download and install ngrok")
        print("   4. Add your auth token: ngrok authtoken YOUR_TOKEN")
        return False

def create_public_url(port=8080):
    """Create a public URL using ngrok"""
    print(f"🌐 Creating public URL for port {port}...")
    
    try:
        # Start ngrok tunnel
        ngrok_process = subprocess.Popen([
            'ngrok', 'http', str(port), '--log=stdout'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for ngrok to start
        time.sleep(3)
        
        # Get the public URL from ngrok API
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                
                if tunnels:
                    public_url = tunnels[0]['public_url']
                    print(f"✅ Public URL created: {public_url}")
                    print(f"🔗 Your Schedule Creator is now accessible at: {public_url}")
                    
                    # Open in browser
                    webbrowser.open(public_url)
                    
                    return public_url, ngrok_process
                else:
                    print("❌ No tunnels found")
                    return None, ngrok_process
            else:
                print("❌ Failed to get tunnel information")
                return None, ngrok_process
                
        except requests.RequestException as e:
            print(f"❌ Error getting tunnel info: {e}")
            return None, ngrok_process
            
    except Exception as e:
        print(f"❌ Error creating ngrok tunnel: {e}")
        return None, None

def main():
    """Main function to create public URL"""
    print("🌐 Schedule Creator - Public URL Generator")
    print("=" * 50)
    
    # Check if Flask app is running
    try:
        response = requests.get('http://localhost:8080/', timeout=2)
        if response.status_code == 200:
            print("✅ Flask application is running on localhost:8080")
        else:
            print("⚠️  Flask application may not be running")
    except requests.RequestException:
        print("❌ Flask application is not running on localhost:8080")
        print("💡 Please start your Schedule Creator first:")
        print("   python schedule_creator_app.py")
        return
    
    # Install ngrok
    if not install_ngrok():
        return
    
    # Create public URL
    public_url, ngrok_process = create_public_url()
    
    if public_url:
        print("\n🎉 SUCCESS!")
        print("=" * 30)
        print(f"🌐 Public URL: {public_url}")
        print("📱 Access your Schedule Creator from anywhere!")
        print("🔄 The URL will remain active as long as ngrok is running")
        print("\n💡 To stop the public URL:")
        print("   Press Ctrl+C or close this terminal")
        print("\n🔧 To make it permanent:")
        print("   1. Sign up for ngrok account")
        print("   2. Use: ngrok http 8080 --domain=your-custom-domain")
        
        try:
            # Keep the process running
            ngrok_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping ngrok tunnel...")
            ngrok_process.terminate()
            print("✅ Public URL stopped")
    else:
        print("❌ Failed to create public URL")

if __name__ == '__main__':
    main()
