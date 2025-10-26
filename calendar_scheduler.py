#!/usr/bin/env python3
"""
Google Calendar Schedule Creator
Creates detailed work schedule for the week with bootcamp constraints
"""

import os
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
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(service, title, start_time, end_time, description="", location=""):
    """Create a calendar event"""
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/New_York',  # Adjust timezone as needed
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/New_York',  # Adjust timezone as needed
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                {'method': 'popup', 'minutes': 30},       # 30 minutes before
            ],
        },
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
    return event

def create_work_schedule():
    """Create the complete work schedule"""
    
    # Get current date and calculate the week
    today = datetime.now()
    # Find the next Sunday (or current Sunday if today is Sunday)
    days_ahead = 6 - today.weekday()  # Sunday is 6
    if days_ahead == 7:  # If today is Sunday
        days_ahead = 0
    elif days_ahead > 0:  # If we're past Sunday this week
        days_ahead -= 7
    
    sunday = today + timedelta(days=days_ahead)
    
    # Authenticate
    service = authenticate_google_calendar()
    
    # Schedule for each day
    schedule = [
        # Sunday
        {
            'date': sunday,
            'events': [
                {
                    'title': 'Carried Over JIRA - Git Comparison & Test Analysis',
                    'start': '09:00',
                    'end': '13:00',
                    'description': 'Compare with original branch, analyze test failures across 10-15 files, document root causes'
                },
                {
                    'title': 'Use Case Analysis & Documentation',
                    'start': '14:00',
                    'end': '18:00',
                    'description': 'Analyze all use cases, draft comprehensive documentation, plan implementation'
                }
            ]
        },
        # Monday
        {
            'date': sunday + timedelta(days=1),
            'events': [
                {
                    'title': 'Use Case Implementation',
                    'start': '09:00',
                    'end': '13:00',
                    'description': 'Complete use case documentation, begin coding implementation'
                },
                {
                    'title': 'Integration Testing Setup',
                    'start': '14:00',
                    'end': '18:00',
                    'description': 'Set up testing environment, begin integration testing for carried over JIRA'
                }
            ]
        },
        # Tuesday
        {
            'date': sunday + timedelta(days=2),
            'events': [
                {
                    'title': 'Bootcamp Session',
                    'start': '08:00',
                    'end': '13:00',
                    'description': 'Bootcamp training session',
                    'location': 'Bootcamp Location'
                },
                {
                    'title': 'Development & Testing',
                    'start': '14:00',
                    'end': '19:00',
                    'description': 'Complete use case coding, continue integration testing, work on regular JIRAs'
                }
            ]
        },
        # Wednesday
        {
            'date': sunday + timedelta(days=3),
            'events': [
                {
                    'title': 'Final Development Push',
                    'start': '09:00',
                    'end': '13:00',
                    'description': 'Complete integration testing, finish regular JIRAs'
                },
                {
                    'title': 'Review & Submission',
                    'start': '14:00',
                    'end': '18:00',
                    'description': 'Final review of all work, submit review comments response, buffer time for issues'
                }
            ]
        },
        # Thursday
        {
            'date': sunday + timedelta(days=4),
            'events': [
                {
                    'title': 'Bootcamp Session',
                    'start': '08:00',
                    'end': '13:00',
                    'description': 'Bootcamp training session',
                    'location': 'Bootcamp Location'
                },
                {
                    'title': 'Wrap-up & Documentation',
                    'start': '14:00',
                    'end': '19:00',
                    'description': 'Complete any remaining tasks, final documentation, code review submissions'
                }
            ]
        }
    ]
    
    # Create events
    for day_schedule in schedule:
        date = day_schedule['date']
        for event in day_schedule['events']:
            start_time = datetime.combine(date, datetime.strptime(event['start'], '%H:%M').time())
            end_time = datetime.combine(date, datetime.strptime(event['end'], '%H:%M').time())
            
            create_calendar_event(
                service=service,
                title=event['title'],
                start_time=start_time,
                end_time=end_time,
                description=event['description'],
                location=event.get('location', '')
            )
    
    print("✅ All calendar events created successfully!")
    print(f"📅 Schedule created for week starting: {sunday.strftime('%A, %B %d, %Y')}")

if __name__ == '__main__':
    print("🚀 Creating your work schedule in Google Calendar...")
    create_work_schedule()
