#!/usr/bin/env python3
"""
Adjust schedule: Sleep at 10:30 PM, wake at 7:30 AM (9 hours)
Events start at 9:00 AM after breakfast
"""

import os
import pickle
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    """Authenticate with Google Calendar"""
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    
    return build('calendar', 'v3', credentials=creds)

def create_event(service, title, start_time, end_time, description="", color_id=None):
    """Create a calendar event"""
    timezone = pytz.timezone('America/New_York')
    
    if start_time.tzinfo is None:
        start_time = timezone.localize(start_time)
    if end_time.tzinfo is None:
        end_time = timezone.localize(end_time)
    
    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }
    
    if color_id:
        event['colorId'] = color_id
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'✅ Created: {title} at {start_time.strftime("%I:%M %p")} - {end_time.strftime("%I:%M %p")}')
        return event.get('id')
    except Exception as e:
        print(f'❌ Error creating {title}: {e}')
        return None

def delete_existing_schedule(service):
    """Remove existing schedule"""
    today_start = datetime(2025, 10, 26, 0, 0, 0)
    today_end = datetime(2025, 10, 28, 0, 0, 0)
    
    timezone = pytz.timezone('America/New_York')
    today_start = timezone.localize(today_start)
    today_end = timezone.localize(today_end)
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=today_start.isoformat(),
        timeMax=today_end.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    print(f"\n🗑️  Removing {len(events)} existing events...\n")
    
    for event in events:
        try:
            event_title = event.get('summary', 'Untitled')
            service.events().delete(calendarId='primary', eventId=event['id']).execute()
            print(f"   ✅ Removed: {event_title}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n   ✅ Existing schedule removed\n")

def main():
    print("🔄 Creating schedule with proper sleep timing")
    print("📅 Date: October 26, 2025 (Sunday)")
    print("😴 Sleep: 10:30 PM - 7:30 AM (9 hours)")
    print("📅 Events start: 9:00 AM (after 9-hour sleep)\n")
    
    service = authenticate()
    delete_existing_schedule(service)
    
    # Sleep from previous night (Oct 25 -> Oct 26)
    schedule = [
        # Saturday night: 10:30 PM - 7:30 AM (9 hours sleep)
        {
            'title': '😴 Sleep (9 hours)',
            'start': datetime(2025, 10, 25, 22, 30),
            'duration': timedelta(hours=9),
            'description': 'Rest and recovery - 9 hours of sleep',
            'color': '4'
        },
    ]
    
    # Sunday Oct 26, events starting at 9 AM
    schedule.extend([
        # 9:00 AM - 10:00 AM: Morning Routine & Breakfast
        {
            'title': '🌅 Morning Routine & Breakfast',
            'start': datetime(2025, 10, 26, 9, 0),
            'duration': timedelta(hours=1),
            'description': 'Start your day with a healthy routine',
            'color': '9'
        },
        
        # 10:00 AM - 11:00 AM: Deep Work Session 1
        {
            'title': '💻 Deep Work Session 1',
            'start': datetime(2025, 10, 26, 10, 0),
            'duration': timedelta(hours=1),
            'description': 'Focused work time',
            'color': '5'
        },
        
        # 11:00 AM - 11:30 AM: Break
        {
            'title': '☕ Break (30 min)',
            'start': datetime(2025, 10, 26, 11, 0),
            'duration': timedelta(minutes=30),
            'description': 'Rest and recharge',
            'color': '9'
        },
        
        # 11:30 AM - 1:00 PM: Deep Work Session 2
        {
            'title': '💻 Deep Work Session 2',
            'start': datetime(2025, 10, 26, 11, 30),
            'duration': timedelta(hours=1, minutes=30),
            'description': 'Focused work time',
            'color': '5'
        },
        
        # 1:00 PM - 2:00 PM: Lunch
        {
            'title': '🍽️ Lunch Break',
            'start': datetime(2025, 10, 26, 13, 0),
            'duration': timedelta(hours=1),
            'description': 'Enjoy a healthy lunch',
            'color': '10'
        },
        
        # 2:00 PM - 3:00 PM: Afternoon Focus
        {
            'title': '📚 Afternoon Focus Session',
            'start': datetime(2025, 10, 26, 14, 0),
            'duration': timedelta(hours=1),
            'description': 'Learning or skill development',
            'color': '6'
        },
        
        # 3:00 PM - 4:00 PM: Evening Work Session
        {
            'title': '🔧 Evening Work Session',
            'start': datetime(2025, 10, 26, 15, 0),
            'duration': timedelta(hours=1),
            'description': 'Final productive session',
            'color': '5'
        },
        
        # 4:00 PM - 5:30 PM: Personal Time / Exercise
        {
            'title': '🏃 Personal Time / Exercise',
            'start': datetime(2025, 10, 26, 16, 0),
            'duration': timedelta(hours=1, minutes=30),
            'description': 'Physical activity or relaxation',
            'color': '10'
        },
        
        # 5:30 PM - 6:30 PM: Dinner
        {
            'title': '🍽️ Dinner',
            'start': datetime(2025, 10, 26, 17, 30),
            'duration': timedelta(hours=1),
            'description': 'Evening meal',
            'color': '10'
        },
        
        # 6:30 PM - 8:00 PM: Free Time / Recreation
        {
            'title': '🎬 Free Time / Recreation',
            'start': datetime(2025, 10, 26, 18, 30),
            'duration': timedelta(hours=1, minutes=30),
            'description': 'Relax and unwind',
            'color': '10'
        },
        
        # 8:00 PM - 10:30 PM: Evening Wind Down
        {
            'title': '🌙 Evening Wind Down',
            'start': datetime(2025, 10, 26, 20, 0),
            'duration': timedelta(hours=2, minutes=30),
            'description': 'Prepare for sleep',
            'color': '9'
        },
    ])
    
    print("📅 Creating schedule...\n")
    created_count = 0
    
    for item in schedule:
        end_time = item['start'] + item['duration']
        create_event(service, item['title'], item['start'], end_time, 
                    item['description'], item['color'])
        created_count += 1
    
    work_time = timedelta(hours=0)
    for item in schedule[1:]:  # Skip sleep
        title = item['title']
        if 'Work' in title or 'Focus' in title or 'Deep' in title or 'Session' in title:
            work_time += item['duration']
    
    print(f"\n✅ Successfully created {created_count} events!")
    print(f"📅 Sleep: 10:30 PM (Oct 25) - 7:30 AM (Oct 26) = 9 hours")
    print(f"📅 Events start at 9:00 AM (Oct 26) - after 9-hour sleep")
    print(f"⏰ Total work time: {work_time}")
    print(f"\n📅 Check your Google Calendar!")

if __name__ == '__main__':
    main()
