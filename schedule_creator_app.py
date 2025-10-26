#!/usr/bin/env python3
"""
Schedule Creator Web Application
A clean web UI for creating optimized schedules and managing Google Calendar
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

class ScheduleCreator:
    def __init__(self):
        self.service = None
        
    def authenticate_google_calendar(self):
        """Authenticate and return Google Calendar service"""
        creds = None
        
        # Try to load credentials from environment variable (Railway)
        creds_json_env = os.environ.get('GOOGLE_CREDENTIALS')
        token_env = os.environ.get('GOOGLE_TOKEN')
        
        if creds_json_env and token_env:
            try:
                import base64
                import json
                import io
                print("Loading credentials from environment variables...")
                print(f"Credentials length: {len(creds_json_env)}")
                print(f"Token length: {len(token_env)}")
                
                # Remove quotes if present
                if creds_json_env.startswith('"') and creds_json_env.endswith('"'):
                    creds_json_env = creds_json_env[1:-1]
                if token_env.startswith('"') and token_env.endswith('"'):
                    token_env = token_env[1:-1]
                
                # Decode base64 token
                token_data = base64.b64decode(token_env)
                token_file = io.BytesIO(token_data)
                creds = pickle.load(token_file)
                print("✅ Successfully loaded token from environment")
                print(f"Token valid: {creds.valid if creds else None}")
            except Exception as e:
                print(f"❌ Error loading credentials from environment: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        # Check for existing token file
        if not creds and os.path.exists('token.pickle'):
            try:
                print("Loading token from file...")
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
                print("✅ Successfully loaded token from file")
            except Exception as e:
                print(f"❌ Error loading token file: {e}")
                return None
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    print("🔄 Refreshing expired credentials...")
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    return None
            else:
                print("No valid credentials found")
                return None
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            return self.service
        except Exception as e:
            print(f"Error building calendar service: {e}")
            return None
    
    def create_optimized_schedule(self, schedule_config):
        """Create optimized schedule based on configuration"""
        
        # Check if custom events are provided
        if 'events' in schedule_config and schedule_config['events']:
            return self.create_custom_schedule(schedule_config['events'])
        
        # Get current date and calculate the week
        today = datetime.now()
        days_ahead = 6 - today.weekday()  # Sunday is 6
        if days_ahead == 7:
            days_ahead = 0
        elif days_ahead > 0:
            days_ahead -= 7
        
        sunday = today + timedelta(days=days_ahead)
        
        # Optimized schedule based on research
        optimized_schedule = [
            {
                'date': sunday,
                'day_name': 'Sunday',
                'theme': '📊 ANALYSIS & PLANNING',
                'sessions': [
                    {
                        'title': '🔍 JIRA Analysis - Git Comparison',
                        'start': '09:00',
                        'end': '10:15',
                        'description': 'Deep analysis of JIRA tickets and Git commits',
                        'type': 'high_cognitive'
                    },
                    {
                        'title': '🔍 Test Failure Investigation',
                        'start': '10:30',
                        'end': '11:45',
                        'description': 'Investigate and document test failures',
                        'type': 'high_cognitive'
                    },
                    {
                        'title': '📝 Use Case Documentation',
                        'start': '14:00',
                        'end': '15:15',
                        'description': 'Document use cases and requirements',
                        'type': 'medium_cognitive'
                    },
                    {
                        'title': '📝 Implementation Planning',
                        'start': '15:30',
                        'end': '16:45',
                        'description': 'Plan implementation approach and timeline',
                        'type': 'medium_cognitive'
                    }
                ]
            },
            {
                'date': sunday + timedelta(days=1),
                'day_name': 'Monday',
                'theme': '🔧 DEVELOPMENT FOCUS',
                'sessions': [
                    {
                        'title': '🔧 Core Logic Implementation',
                        'start': '09:00',
                        'end': '10:15',
                        'description': 'Implement core business logic',
                        'type': 'high_cognitive'
                    },
                    {
                        'title': '🔧 Integration Development',
                        'start': '10:30',
                        'end': '11:45',
                        'description': 'Develop integration components',
                        'type': 'high_cognitive'
                    },
                    {
                        'title': '🔍 Test Environment Setup',
                        'start': '14:00',
                        'end': '15:15',
                        'description': 'Set up and configure test environments',
                        'type': 'medium_cognitive'
                    },
                    {
                        'title': '🔍 Integration Test Development',
                        'start': '15:30',
                        'end': '16:45',
                        'description': 'Develop integration tests',
                        'type': 'medium_cognitive'
                    }
                ]
            },
            {
                'date': sunday + timedelta(days=2),
                'day_name': 'Tuesday',
                'theme': '📚 BOOTCAMP & DEVELOPMENT',
                'sessions': [
                    {
                        'title': '📚 Bootcamp Session',
                        'start': '08:00',
                        'end': '13:00',
                        'description': 'Organization-wide bootcamp training',
                        'type': 'learning'
                    },
                    {
                        'title': '🔧 Post-Bootcamp Development',
                        'start': '14:00',
                        'end': '15:15',
                        'description': 'Apply bootcamp learnings to development',
                        'type': 'medium_cognitive'
                    },
                    {
                        'title': '🔍 Testing & Debugging',
                        'start': '15:30',
                        'end': '16:45',
                        'description': 'Test and debug developed features',
                        'type': 'medium_cognitive'
                    },
                    {
                        'title': '🔧 Regular JIRA Tasks',
                        'start': '17:00',
                        'end': '18:15',
                        'description': 'Work on regular JIRA tickets',
                        'type': 'low_cognitive'
                    }
                ]
            },
            {
                'date': sunday + timedelta(days=3),
                'day_name': 'Wednesday',
                'theme': '🔍 TESTING & REVIEW',
                'sessions': [
                    {
                        'title': '🔍 Comprehensive Testing',
                        'start': '09:00',
                        'end': '10:15',
                        'description': 'Execute comprehensive test suite',
                        'type': 'high_cognitive'
                    },
                    {
                        'title': '🔍 Bug Fixing Session',
                        'start': '10:30',
                        'end': '11:45',
                        'description': 'Fix identified bugs and issues',
                        'type': 'high_cognitive'
                    },
                    {
                        'title': '🔧 Final Development Push',
                        'start': '13:00',
                        'end': '14:15',
                        'description': 'Complete remaining development tasks',
                        'type': 'medium_cognitive'
                    },
                    {
                        'title': '🎯 Code Review Preparation',
                        'start': '14:30',
                        'end': '15:45',
                        'description': 'Prepare code for review submission',
                        'type': 'medium_cognitive'
                    }
                ]
            },
            {
                'date': sunday + timedelta(days=4),
                'day_name': 'Thursday',
                'theme': '📚 BOOTCAMP & FINALIZATION',
                'sessions': [
                    {
                        'title': '📚 Bootcamp Session',
                        'start': '08:00',
                        'end': '13:00',
                        'description': 'Organization-wide bootcamp training',
                        'type': 'learning'
                    },
                    {
                        'title': '🎯 Final Review & Submission',
                        'start': '14:00',
                        'end': '15:15',
                        'description': 'Final code review and submission',
                        'type': 'medium_cognitive'
                    },
                    {
                        'title': '📝 Documentation Finalization',
                        'start': '15:30',
                        'end': '16:45',
                        'description': 'Finalize all documentation',
                        'type': 'low_cognitive'
                    },
                    {
                        'title': '🎯 Project Wrap-up',
                        'start': '17:00',
                        'end': '18:15',
                        'description': 'Project closure and wrap-up activities',
                        'type': 'low_cognitive'
                    }
                ]
            }
        ]
        
        return optimized_schedule
    
    def create_custom_schedule(self, events):
        """Create schedule from custom events"""
        schedule = []
        
        # Group events by date
        events_by_date = {}
        for event in events:
            date_str = event['date']
            if date_str not in events_by_date:
                events_by_date[date_str] = []
            events_by_date[date_str].append(event)
        
        # Convert to schedule format
        for date_str, day_events in events_by_date.items():
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            day_name = date_obj.strftime('%A')
            
            sessions = []
            for event in day_events:
                start_time = event['time']
                duration = event.get('duration', 60)
                
                # Calculate end time
                start_hour, start_min = map(int, start_time.split(':'))
                start_minutes = start_hour * 60 + start_min
                end_minutes = start_minutes + duration
                end_hour = end_minutes // 60
                end_min = end_minutes % 60
                end_time = f"{end_hour:02d}:{end_min:02d}"
                
                sessions.append({
                    'title': event['title'],
                    'start': start_time,
                    'end': end_time,
                    'description': event.get('description', event['title']),
                    'type': event.get('type', 'custom')
                })
            
            schedule.append({
                'date': date_obj,
                'day_name': day_name,
                'theme': f'📅 {day_name} Schedule',
                'sessions': sessions
            })
        
        return schedule
    
    def save_schedule_to_calendar(self, schedule):
        """Save schedule to Google Calendar"""
        if not self.service:
            return False, "Google Calendar not authenticated"
        
        try:
            # Get primary calendar
            calendar_list = self.service.calendarList().list().execute()
            primary_calendar_id = None
            
            for calendar in calendar_list.get('items', []):
                if calendar.get('primary'):
                    primary_calendar_id = calendar['id']
                    break
            
            if not primary_calendar_id:
                return False, "Primary calendar not found"
            
            created_count = 0
            
            for day_schedule in schedule:
                for session in day_schedule['sessions']:
                    event = {
                        'summary': session['title'],
                        'description': f"{session['description']}\n\n📊 Session Type: {session['type']}\n⏰ Duration: 75 minutes\n🎯 Optimized for productivity",
                        'start': {
                            'dateTime': f"{day_schedule['date'].strftime('%Y-%m-%d')}T{session['start']}:00",
                            'timeZone': 'America/New_York',
                        },
                        'end': {
                            'dateTime': f"{day_schedule['date'].strftime('%Y-%m-%d')}T{session['end']}:00",
                            'timeZone': 'America/New_York',
                        },
                        'reminders': {
                            'useDefault': False,
                            'overrides': [
                                {'method': 'email', 'minutes': 1440},
                                {'method': 'popup', 'minutes': 15},
                            ],
                        },
                    }
                    
                    try:
                        self.service.events().insert(
                            calendarId=primary_calendar_id,
                            body=event
                        ).execute()
                        created_count += 1
                    except Exception as e:
                        print(f"❌ Failed to create '{session['title']}': {e}")
            
            return True, f"Successfully created {created_count} events"
            
        except Exception as e:
            return False, f"Error saving to calendar: {e}"
    
    def save_schedule_to_file(self, schedule):
        """Save schedule to JSON file"""
        try:
            schedule_data = {
                'created_at': datetime.now().isoformat(),
                'schedule': []
            }
            
            for day_schedule in schedule:
                day_data = {
                    'date': day_schedule['date'].strftime('%Y-%m-%d'),
                    'day_name': day_schedule['day_name'],
                    'theme': day_schedule['theme'],
                    'sessions': day_schedule['sessions']
                }
                schedule_data['schedule'].append(day_data)
            
            with open('schedule_backup.json', 'w') as f:
                json.dump(schedule_data, f, indent=2)
            
            return True, "Schedule saved to schedule_backup.json"
            
        except Exception as e:
            return False, f"Error saving schedule: {e}"

# Global schedule creator instance
schedule_creator = ScheduleCreator()

@app.route('/')
def index():
    """Main page"""
    return render_template('schedule_creator.html')

@app.route('/api/test-credentials')
def test_credentials():
    """Test if credentials are loaded"""
    creds_exists = os.environ.get('GOOGLE_CREDENTIALS') is not None
    token_exists = os.environ.get('GOOGLE_TOKEN') is not None
    
    return jsonify({
        'credentials_set': creds_exists,
        'token_set': token_exists,
        'both_set': creds_exists and token_exists
    })

@app.route('/api/get-calendar-events')
def get_calendar_events():
    """Get calendar events from Google Calendar"""
    try:
        service = schedule_creator.authenticate_google_calendar()
        if not service:
            return jsonify({'success': False, 'message': 'Not authenticated'})
        
        # Get events for the next 7 days
        now = datetime.now()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(days=7)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Format events
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            formatted_events.append({
                'title': event.get('summary', 'No Title'),
                'start': start,
                'end': end,
                'description': event.get('description', '')
            })
        
        return jsonify({'success': True, 'events': formatted_events})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/auth/google')
def auth_google():
    """Authenticate with Google Calendar"""
    try:
        service = schedule_creator.authenticate_google_calendar()
        if service:
            return jsonify({
                'success': True, 
                'message': 'Google Calendar authenticated successfully',
                'info': 'To use this feature, you need credentials.json and token.pickle files from Google Cloud Console'
            })
        else:
            return jsonify({
                'success': False, 
                'message': 'Google Calendar authentication failed',
                'info': 'Missing credentials.json or token.pickle. Please add these files to your deployment for Google Calendar integration to work.'
            })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Authentication error: {str(e)}',
            'info': 'Google Calendar authentication requires credentials.json and token.pickle files'
        })

@app.route('/api/create-schedule', methods=['POST'])
def create_schedule():
    """Create optimized schedule"""
    try:
        data = request.get_json()
        
        # Create optimized schedule
        schedule = schedule_creator.create_optimized_schedule(data)
        
        # Save to calendar
        calendar_success, calendar_message = schedule_creator.save_schedule_to_calendar(schedule)
        
        # Save to file
        file_success, file_message = schedule_creator.save_schedule_to_file(schedule)
        
        return jsonify({
            'success': calendar_success and file_success,
            'schedule': schedule,
            'calendar_message': calendar_message,
            'file_message': file_message
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating schedule: {e}'})


if __name__ == '__main__':
    # Only run Flask dev server if not in production
    if os.environ.get('FLASK_ENV') != 'production':
        print("🚀 Starting Schedule Creator Web Application (Dev Mode)...")
        port = int(os.environ.get('PORT', 8080))
        host = os.environ.get('HOST', '0.0.0.0')
        print(f"📱 Server running on http://{host}:{port}")
        app.run(debug=True, host=host, port=port)
    else:
        # In production, gunicorn will be used
        print("Production mode - use 'gunicorn schedule_creator_app:app' to start")
