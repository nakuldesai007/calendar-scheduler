#!/usr/bin/env python3
"""
Mac Calendar Integration Checker
Verifies that your Google Calendar is properly synced with Mac Calendar
"""

import os
import subprocess
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Authenticate and return Google Calendar service"""
    creds = None
    
    # Check for existing token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🌐 Opening browser for authentication...")
            print("📋 Please complete the OAuth flow in your browser.")
            
            if os.path.exists('credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                # Try different ports
                for port in [8080, 8081, 8082, 8083, 8084]:
                    try:
                        print(f"🔄 Trying port {port}...")
                        creds = flow.run_local_server(port=port)
                        break
                    except Exception as e:
                        print(f"❌ Port {port} failed: {e}")
                        continue
                else:
                    print("❌ All ports failed. Please check your OAuth2 configuration.")
                    return None
            else:
                print("❌ No credentials.json found!")
                return None
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        print("✅ Authentication successful!")

    service = build('calendar', 'v3', credentials=creds)
    return service

def check_mac_calendar_sync():
    """Check if Google Calendar is synced with Mac Calendar"""
    
    print("🍎 MAC CALENDAR INTEGRATION CHECK")
    print("=" * 50)
    
    # Check if Google Calendar is set up in Mac Calendar
    try:
        # Use AppleScript to check calendar accounts
        script = '''
        tell application "Calendar"
            set accountList to every account
            set googleAccounts to {}
            repeat with anAccount in accountList
                if class of anAccount is caldav account then
                    set accountName to name of anAccount
                    if accountName contains "Google" or accountName contains "gmail" then
                        set end of googleAccounts to accountName
                    end if
                end if
            end repeat
            return googleAccounts
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            google_accounts = result.stdout.strip().split(', ')
            print(f"✅ Found Google Calendar accounts: {', '.join(google_accounts)}")
            return True
        else:
            print("❌ No Google Calendar accounts found in Mac Calendar")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Mac Calendar: {e}")
        return False

def check_calendar_visibility():
    """Check if calendars are visible in Mac Calendar"""
    
    print("\n📅 CHECKING CALENDAR VISIBILITY")
    print("-" * 40)
    
    try:
        # Check if calendars are visible
        script = '''
        tell application "Calendar"
            set calendarList to every calendar
            set visibleCalendars to {}
            repeat with aCalendar in calendarList
                if visible of aCalendar is true then
                    set end of visibleCalendars to name of aCalendar
                end if
            end repeat
            return visibleCalendars
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            visible_calendars = result.stdout.strip().split(', ')
            print(f"📋 Visible calendars: {', '.join(visible_calendars)}")
            
            # Check if primary calendar is visible
            primary_calendar = None
            for cal in visible_calendars:
                if '@gmail.com' in cal or 'nakuldesai007' in cal:
                    primary_calendar = cal
                    break
            
            if primary_calendar:
                print(f"✅ Primary calendar '{primary_calendar}' is visible")
                return True
            else:
                print("⚠️  Primary calendar not found in visible calendars")
                return False
        else:
            print("❌ No visible calendars found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking calendar visibility: {e}")
        return False

def open_mac_calendar():
    """Open Mac Calendar application"""
    
    print("\n🍎 OPENING MAC CALENDAR")
    print("-" * 30)
    
    try:
        subprocess.run(['open', '-a', 'Calendar'], check=True)
        print("✅ Mac Calendar opened successfully")
        return True
    except Exception as e:
        print(f"❌ Error opening Mac Calendar: {e}")
        return False

def get_google_calendar_events(service):
    """Get events from Google Calendar to verify sync"""
    
    print("\n📊 CHECKING GOOGLE CALENDAR EVENTS")
    print("-" * 40)
    
    # Get current date and calculate the week
    today = datetime.now()
    # Find the next Sunday (or current Sunday if today is Sunday)
    days_ahead = 6 - today.weekday()  # Sunday is 6
    if days_ahead == 7:  # If today is Sunday
        days_ahead = 0
    elif days_ahead > 0:  # If we're past Sunday this week
        days_ahead -= 7
    
    sunday = today + timedelta(days=days_ahead)
    
    try:
        # Get primary calendar
        calendar_list = service.calendarList().list().execute()
        primary_calendar_id = None
        
        for calendar in calendar_list.get('items', []):
            if calendar.get('primary'):
                primary_calendar_id = calendar['id']
                break
        
        if not primary_calendar_id:
            print("❌ Primary calendar not found")
            return []
        
        # Get events for the entire week
        start_date = sunday.replace(hour=0, minute=0, second=0)
        end_date = sunday + timedelta(days=4)  # Thursday
        end_date = end_date.replace(hour=23, minute=59, second=59)
        
        time_min = start_date.isoformat() + 'Z'
        time_max = end_date.isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=primary_calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        print(f"📅 Found {len(events)} events in Google Calendar for this week")
        
        if events:
            print("📋 Recent events:")
            for event in events[:5]:  # Show first 5
                start_time_str = event.get('start', {}).get('dateTime', '')
                if start_time_str:
                    start_time = datetime.fromisoformat(start_time_str.replace('Z', '').split('+')[0])
                    print(f"   {start_time.strftime('%Y-%m-%d %H:%M')} - {event.get('summary', 'Untitled')}")
        
        return events
        
    except Exception as e:
        print(f"❌ Error getting Google Calendar events: {e}")
        return []

def provide_sync_instructions():
    """Provide instructions for syncing Google Calendar with Mac Calendar"""
    
    print("\n📋 GOOGLE CALENDAR SYNC INSTRUCTIONS")
    print("=" * 50)
    
    print("🔧 To sync your Google Calendar with Mac Calendar:")
    print()
    print("1️⃣ **Add Google Account to Mac Calendar:**")
    print("   • Open Mac Calendar app")
    print("   • Go to Calendar → Add Account...")
    print("   • Select 'Google'")
    print("   • Sign in with your Google account (nakuldesai007@gmail.com)")
    print("   • Make sure 'Calendars' is checked")
    print()
    print("2️⃣ **Verify Calendar Visibility:**")
    print("   • In Mac Calendar, check the left sidebar")
    print("   • Make sure your Google calendar is checked/visible")
    print("   • Look for calendars with your email address")
    print()
    print("3️⃣ **Check Sync Settings:**")
    print("   • Go to Calendar → Preferences → Accounts")
    print("   • Select your Google account")
    print("   • Make sure 'Enable this account' is checked")
    print("   • Set refresh interval to 'Push' or 'Every 15 minutes'")
    print()
    print("4️⃣ **Verify Events Appear:**")
    print("   • Navigate to the current week in Mac Calendar")
    print("   • Look for your work schedule events")
    print("   • Events should appear with emojis (🔍, 🔧, 📚, etc.)")
    print()
    print("💡 **Benefits of Mac Calendar Integration:**")
    print("   • Native Mac notifications")
    print("   • Integration with Focus modes")
    print("   • Siri integration")
    print("   • Menu bar calendar widget")
    print("   • Desktop notifications")

def main():
    """Main function to check Mac Calendar integration"""
    print("🍎 Mac Calendar Integration Checker")
    print("=" * 40)
    
    # Authenticate with Google Calendar
    service = authenticate_google_calendar()
    if not service:
        print("❌ Failed to authenticate with Google Calendar")
        return
    
    # Check Mac Calendar sync
    mac_sync = check_mac_calendar_sync()
    
    # Check calendar visibility
    calendar_visible = check_calendar_visibility()
    
    # Get Google Calendar events
    events = get_google_calendar_events(service)
    
    # Open Mac Calendar
    open_mac_calendar()
    
    # Provide instructions
    provide_sync_instructions()
    
    print("\n🎯 SUMMARY:")
    print("=" * 20)
    print(f"Google Calendar Sync: {'✅ Yes' if mac_sync else '❌ No'}")
    print(f"Calendar Visible: {'✅ Yes' if calendar_visible else '❌ No'}")
    print(f"Events Found: {'✅ Yes' if events else '❌ No'}")
    
    if mac_sync and calendar_visible and events:
        print("\n🎉 PERFECT! Your Google Calendar is fully integrated with Mac Calendar!")
        print("📱 You can now see your optimized schedule in both:")
        print("   • Web Dashboard: http://localhost:8080")
        print("   • Mac Calendar app")
    else:
        print("\n⚠️  Some integration issues detected. Follow the instructions above to fix them.")

if __name__ == '__main__':
    main()
