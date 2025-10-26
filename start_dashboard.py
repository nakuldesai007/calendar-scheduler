#!/usr/bin/env python3
"""
Productivity Dashboard Launcher
Simple launcher for the productivity dashboard
"""

import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("🚀 Starting Productivity Dashboard...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('dashboard_server.py'):
        print("❌ dashboard_server.py not found!")
        print("Please run this script from the calendar-scheduler directory")
        return
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("❌ Virtual environment not found!")
        print("Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt")
        return
    
    # Check if credentials exist
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please ensure your Google Calendar API credentials are set up")
        return
    
    print("✅ All prerequisites found!")
    print()
    print("🌐 Starting dashboard server...")
    print("📱 The dashboard will open in your browser automatically")
    print("🔄 Dashboard refreshes every 30 seconds")
    print()
    print("💡 Features:")
    print("   • Real-time schedule overview")
    print("   • Current task tracking")
    print("   • Progress monitoring")
    print("   • Weekly schedule view")
    print("   • Productivity statistics")
    print()
    
    # Start the server
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:8080')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the Flask server
        subprocess.run([
            sys.executable, 'dashboard_server.py'
        ], cwd=os.getcwd())
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

if __name__ == '__main__':
    main()
