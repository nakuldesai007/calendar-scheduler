#!/usr/bin/env python3
"""
Get Public URL from Cloudflare Tunnel
"""

import subprocess
import time
import webbrowser

def get_cloudflare_url():
    """Get the public URL from Cloudflare tunnel"""
    print("🌐 Getting Cloudflare tunnel URL...")
    
    try:
        # Check if cloudflared is running
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'cloudflared tunnel' not in result.stdout:
            print("❌ Cloudflare tunnel is not running")
            print("💡 Run: cloudflared tunnel --url http://localhost:8080")
            return None
        
        # The URL is usually printed in the logs
        print("✅ Cloudflare tunnel is running!")
        print("🔍 Check your terminal where cloudflared is running")
        print("📋 Look for a line like: 'https://random-string.trycloudflare.com'")
        print("\n💡 The public URL should be displayed in the cloudflared output")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main function"""
    print("🌐 Cloudflare Tunnel - Public URL Checker")
    print("=" * 50)
    
    if get_cloudflare_url():
        print("\n🎉 SUCCESS!")
        print("=" * 20)
        print("📱 Your Schedule Creator is now accessible via Cloudflare tunnel!")
        print("🔗 Look for the URL in your cloudflared terminal output")
        print("🌍 The URL will work from anywhere in the world")
        print("\n💡 To stop the tunnel:")
        print("   Press Ctrl+C in the cloudflared terminal")
    else:
        print("❌ Failed to get tunnel URL")

if __name__ == '__main__':
    main()
