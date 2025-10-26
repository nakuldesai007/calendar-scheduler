#!/usr/bin/env python3
"""
Get ngrok Public URL and Open Schedule Creator
"""

import requests
import webbrowser
import time
import subprocess

def get_ngrok_url():
    """Get the public URL from ngrok"""
    print("🌐 Getting ngrok public URL...")
    
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                
                if tunnels:
                    # Get the HTTPS tunnel
                    for tunnel in tunnels:
                        if tunnel.get('proto') == 'https':
                            public_url = tunnel['public_url']
                            print(f"✅ Found public URL: {public_url}")
                            return public_url
                    
                    # If no HTTPS, get HTTP
                    if tunnels:
                        public_url = tunnels[0]['public_url']
                        print(f"✅ Found public URL: {public_url}")
                        return public_url
                else:
                    print(f"⏳ Waiting for tunnel... ({i+1}/{max_retries})")
                    time.sleep(2)
            else:
                print(f"⏳ ngrok not ready yet... ({i+1}/{max_retries})")
                time.sleep(2)
        except requests.RequestException:
            print(f"⏳ ngrok starting... ({i+1}/{max_retries})")
            time.sleep(2)
    
    print("❌ Could not get ngrok URL")
    return None

def open_schedule_creator(url):
    """Open the Schedule Creator in browser"""
    print(f"🚀 Opening Schedule Creator: {url}")
    webbrowser.open(url)
    print("✅ Schedule Creator opened in your browser!")

def main():
    """Main function"""
    print("🚀 Schedule Creator - ngrok Deployment")
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
    
    # Get ngrok URL
    public_url = get_ngrok_url()
    
    if public_url:
        print("\n🎉 SUCCESS!")
        print("=" * 30)
        print(f"🌐 Public URL: {public_url}")
        print("📱 Your Schedule Creator is now live!")
        print("🌍 Accessible from anywhere in the world")
        
        # Open in browser
        open_schedule_creator(public_url)
        
        print("\n💡 Share this URL with anyone:")
        print(f"   {public_url}")
        print("\n🔄 The URL will remain active as long as ngrok is running")
        print("🛑 To stop: Press Ctrl+C in the ngrok terminal")
        
    else:
        print("❌ Failed to get public URL")
        print("💡 Try manually:")
        print("   1. Check ngrok terminal for the URL")
        print("   2. Or visit: http://localhost:4040")

if __name__ == '__main__':
    main()
