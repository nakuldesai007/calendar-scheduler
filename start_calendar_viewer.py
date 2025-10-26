#!/usr/bin/env python3
"""Quick start script for the Calendar Viewer"""
import webbrowser
import time
import subprocess

print("🚀 Starting Calendar Viewer UI...")
print("📱 Opening browser in 3 seconds...\n")

time.sleep(3)
webbrowser.open('http://localhost:8080/calendar-viewer')

print("✅ Calendar Viewer should be open in your browser!")
print("📍 URL: http://localhost:8080/calendar-viewer")
