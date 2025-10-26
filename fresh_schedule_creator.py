#!/usr/bin/env python3
"""
Fresh Work Schedule Creator
Creates a clean, organized work schedule from scratch
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

def create_work_calendars(service):
    """Create clean work calendars"""
    
    calendars = [
        {
            'name': '🔧 Development Work',
            'description': 'Focused development sessions, coding, and technical implementation',
            'color': '#4285f4'  # Blue
        },
        {
            'name': '📚 Bootcamp Sessions',
            'description': 'Organization-wide bootcamp training sessions',
            'color': '#34a853'  # Green
        },
        {
            'name': '🔍 Analysis & Testing',
            'description': 'Code analysis, testing, debugging, and quality assurance',
            'color': '#fbbc04'  # Yellow
        },
        {
            'name': '📝 Documentation & Planning',
            'description': 'Documentation, planning, and project management tasks',
            'color': '#ea4335'  # Red
        },
        {
            'name': '🎯 Review & Submission',
            'description': 'Code reviews, submissions, and final deliverables',
            'color': '#9c27b0'  # Purple
        }
    ]
    
    created_calendars = {}
    
    print("📅 Creating fresh work calendars...")
    for calendar_info in calendars:
        calendar = {
            'summary': calendar_info['name'],
            'description': calendar_info['description'],
            'timeZone': 'America/New_York'
        }
        
        try:
            created_calendar = service.calendars().insert(body=calendar).execute()
            calendar_id = created_calendar['id']
            created_calendars[calendar_info['name']] = calendar_id
            print(f"✅ Created: {calendar_info['name']}")
        except Exception as e:
            print(f"❌ Failed to create '{calendar_info['name']}': {e}")
    
    return created_calendars

def create_calendar_event(service, calendar_id, title, start_time, end_time, description="", location=""):
    """Create a calendar event"""
    event = {
        'summary': title,
        'location': location,
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
                {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                {'method': 'popup', 'minutes': 15},       # 15 minutes before
            ],
        },
    }
    
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'✅ Event created: {event.get("htmlLink")}')
    return event

def create_fresh_work_schedule():
    """Create a fresh, clean work schedule"""
    
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
    if not service:
        print("❌ Authentication failed. Please check your OAuth2 configuration.")
        return
    
    # Create fresh calendars
    calendars = create_work_calendars(service)
    
    if not calendars:
        print("❌ Failed to create calendars.")
        return
    
    print(f"\n📅 Creating fresh schedule for week starting: {sunday.strftime('%A, %B %d, %Y')}")
    
    # Clean, organized schedule
    schedule = [
        # Sunday - Analysis & Planning Day
        {
            'date': sunday,
            'sessions': [
                {
                    'calendar': '🔍 Analysis & Testing',
                    'title': 'JIRA Analysis - Git Comparison',
                    'start': '09:00',
                    'end': '10:30',
                    'description': 'Deep dive into git differences, identify root causes of test failures'
                },
                {
                    'calendar': '🔍 Analysis & Testing',
                    'title': 'Test Failure Investigation',
                    'start': '10:45',
                    'end': '12:15',
                    'description': 'Analyze 10-15 test files, document patterns and issues'
                },
                {
                    'calendar': '📝 Documentation & Planning',
                    'title': 'Use Case Documentation',
                    'start': '14:00',
                    'end': '15:30',
                    'description': 'Draft comprehensive use case documentation'
                },
                {
                    'calendar': '📝 Documentation & Planning',
                    'title': 'Implementation Planning',
                    'start': '15:45',
                    'end': '17:15',
                    'description': 'Plan implementation approach and timeline'
                }
            ]
        },
        # Monday - Development Focus Day
        {
            'date': sunday + timedelta(days=1),
            'sessions': [
                {
                    'calendar': '🔧 Development Work',
                    'title': 'Use Case Implementation - Core Logic',
                    'start': '09:00',
                    'end': '10:30',
                    'description': 'Implement core use case business logic'
                },
                {
                    'calendar': '🔧 Development Work',
                    'title': 'Use Case Implementation - Integration',
                    'start': '10:45',
                    'end': '12:15',
                    'description': 'Integrate use case with existing systems'
                },
                {
                    'calendar': '🔍 Analysis & Testing',
                    'title': 'Test Environment Setup',
                    'start': '14:00',
                    'end': '15:30',
                    'description': 'Configure testing environment and tools'
                },
                {
                    'calendar': '🔍 Analysis & Testing',
                    'title': 'Integration Test Development',
                    'start': '15:45',
                    'end': '17:15',
                    'description': 'Write and configure integration tests'
                }
            ]
        },
        # Tuesday - Bootcamp Day
        {
            'date': sunday + timedelta(days=2),
            'sessions': [
                {
                    'calendar': '📚 Bootcamp Sessions',
                    'title': 'Bootcamp Session',
                    'start': '08:00',
                    'end': '13:00',
                    'description': 'Organization-wide bootcamp training session',
                    'location': 'Bootcamp Location'
                },
                {
                    'calendar': '🔧 Development Work',
                    'title': 'Post-Bootcamp Development',
                    'start': '14:00',
                    'end': '15:30',
                    'description': 'Apply bootcamp learnings to development work'
                },
                {
                    'calendar': '🔍 Analysis & Testing',
                    'title': 'Testing & Debugging',
                    'start': '15:45',
                    'end': '17:15',
                    'description': 'Execute tests and debug issues'
                },
                {
                    'calendar': '🔧 Development Work',
                    'title': 'Regular JIRA Tasks',
                    'start': '17:30',
                    'end': '19:00',
                    'description': 'Work on regular JIRA tickets'
                }
            ]
        },
        # Wednesday - Testing & Review Day (Unavailable 4PM-7PM)
        {
            'date': sunday + timedelta(days=3),
            'sessions': [
                {
                    'calendar': '🔍 Analysis & Testing',
                    'title': 'Comprehensive Testing',
                    'start': '09:00',
                    'end': '10:30',
                    'description': 'Execute comprehensive test suite'
                },
                {
                    'calendar': '🔍 Analysis & Testing',
                    'title': 'Bug Fixing Session',
                    'start': '10:45',
                    'end': '12:15',
                    'description': 'Fix identified bugs and issues'
                },
                {
                    'calendar': '🔧 Development Work',
                    'title': 'Final Development Push',
                    'start': '13:00',
                    'end': '14:30',
                    'description': 'Complete remaining development tasks'
                },
                {
                    'calendar': '🎯 Review & Submission',
                    'title': 'Code Review Preparation',
                    'start': '14:45',
                    'end': '15:45',
                    'description': 'Prepare code for review submission (Ends before 4PM unavailability)'
                }
            ]
        },
        # Thursday - Bootcamp Day
        {
            'date': sunday + timedelta(days=4),
            'sessions': [
                {
                    'calendar': '📚 Bootcamp Sessions',
                    'title': 'Bootcamp Session',
                    'start': '08:00',
                    'end': '13:00',
                    'description': 'Organization-wide bootcamp training session',
                    'location': 'Bootcamp Location'
                },
                {
                    'calendar': '🎯 Review & Submission',
                    'title': 'Final Review & Submission',
                    'start': '14:00',
                    'end': '15:30',
                    'description': 'Final review and submission of work'
                },
                {
                    'calendar': '📝 Documentation & Planning',
                    'title': 'Documentation Finalization',
                    'start': '15:45',
                    'end': '17:15',
                    'description': 'Complete final documentation'
                },
                {
                    'calendar': '🎯 Review & Submission',
                    'title': 'Project Wrap-up',
                    'start': '17:30',
                    'end': '19:00',
                    'description': 'Final project wrap-up and cleanup'
                }
            ]
        }
    ]
    
    # Create events
    total_events = 0
    for day_schedule in schedule:
        date = day_schedule['date']
        print(f"\n📅 {date.strftime('%A, %B %d')}:")
        
        for session in day_schedule['sessions']:
            start_time = datetime.combine(date, datetime.strptime(session['start'], '%H:%M').time())
            end_time = datetime.combine(date, datetime.strptime(session['end'], '%H:%M').time())
            
            calendar_name = session['calendar']
            if calendar_name in calendars:
                try:
                    create_calendar_event(
                        service=service,
                        calendar_id=calendars[calendar_name],
                        title=session['title'],
                        start_time=start_time,
                        end_time=end_time,
                        description=session['description'],
                        location=session.get('location', '')
                    )
                    total_events += 1
                except Exception as e:
                    print(f"❌ Failed to create event '{session['title']}': {e}")
    
    print(f"\n🎉 Successfully created {total_events} events in fresh calendars!")
    print(f"📅 Schedule created for week starting: {sunday.strftime('%A, %B %d, %Y')}")
    print("\n📋 Your Fresh Calendar Structure:")
    for calendar_name in calendars.keys():
        print(f"  - {calendar_name}")
    
    print("\n🎯 Key Features:")
    print("  - Clean, organized calendars")
    print("  - Bootcamp sessions respect organization timing (8 AM - 1 PM)")
    print("  - Focused 1.5-hour work sessions")
    print("  - Clear separation of work types")
    print("  - Smart reminders (1 day + 15 min before)")

if __name__ == '__main__':
    print("🚀 Creating Fresh Work Schedule...")
    create_fresh_work_schedule()
