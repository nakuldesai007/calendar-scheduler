#!/usr/bin/env python3
"""
Productivity Dashboard Server
A Flask-based web dashboard for schedule overview and progress tracking
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import threading
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

app = Flask(__name__)

class ProductivityDashboard:
    def __init__(self):
        self.service = None
        self.current_week_events = []
        self.last_update = None
        
    def authenticate_google_calendar(self):
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
                print("❌ No valid credentials found!")
                return None
        
        self.service = build('calendar', 'v3', credentials=creds)
        return self.service
    
    def get_current_week_events(self):
        """Get events for current week"""
        if not self.service:
            return []
        
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
            calendar_list = self.service.calendarList().list().execute()
            primary_calendar_id = None
            
            for calendar in calendar_list.get('items', []):
                if calendar.get('primary'):
                    primary_calendar_id = calendar['id']
                    break
            
            if not primary_calendar_id:
                return []
            
            # Get events for the entire week
            start_date = sunday.replace(hour=0, minute=0, second=0)
            end_date = sunday + timedelta(days=4)  # Thursday
            end_date = end_date.replace(hour=23, minute=59, second=59)
            
            time_min = start_date.isoformat() + 'Z'
            time_max = end_date.isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=primary_calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            processed_events = []
            for event in events:
                start_time_str = event.get('start', {}).get('dateTime', '')
                end_time_str = event.get('end', {}).get('dateTime', '')
                
                if start_time_str and end_time_str:
                    # Parse times and handle timezone properly
                    start_time = datetime.fromisoformat(start_time_str.replace('Z', '').split('+')[0])
                    end_time = datetime.fromisoformat(end_time_str.replace('Z', '').split('+')[0])
                    
                    # Make both datetimes timezone-naive for comparison
                    if start_time.tzinfo is not None:
                        start_time = start_time.replace(tzinfo=None)
                    if end_time.tzinfo is not None:
                        end_time = end_time.replace(tzinfo=None)
                    
                    duration = (end_time - start_time).total_seconds() / 3600
                    
                    processed_events.append({
                        'id': event['id'],
                        'title': event.get('summary', 'Untitled'),
                        'start_time': start_time,
                        'end_time': end_time,
                        'start_str': start_time.strftime('%H:%M'),
                        'end_str': end_time.strftime('%H:%M'),
                        'date': start_time.date(),
                        'day_name': start_time.strftime('%A'),
                        'duration': duration,
                        'description': event.get('description', ''),
                        'is_current': self.is_current_event(start_time, end_time),
                        'is_upcoming': self.is_upcoming_event(start_time),
                        'is_completed': self.is_completed_event(end_time)
                    })
            
            self.current_week_events = processed_events
            self.last_update = datetime.now()
            return processed_events
            
        except Exception as e:
            print(f"❌ Error getting events: {e}")
            return []
    
    def is_current_event(self, start_time, end_time):
        """Check if event is currently happening"""
        now = datetime.now()
        return start_time <= now <= end_time
    
    def is_upcoming_event(self, start_time):
        """Check if event is upcoming today"""
        now = datetime.now()
        return start_time > now and start_time.date() == now.date()
    
    def is_completed_event(self, end_time):
        """Check if event is completed"""
        now = datetime.now()
        return end_time < now
    
    def get_productivity_stats(self):
        """Calculate productivity statistics"""
        if not self.current_week_events:
            return {}
        
        total_events = len(self.current_week_events)
        completed_events = len([e for e in self.current_week_events if e['is_completed']])
        current_events = len([e for e in self.current_week_events if e['is_current']])
        upcoming_events = len([e for e in self.current_week_events if e['is_upcoming']])
        
        total_hours = sum(e['duration'] for e in self.current_week_events)
        completed_hours = sum(e['duration'] for e in self.current_week_events if e['is_completed'])
        
        # Calculate completion percentage
        completion_percentage = (completed_events / total_events * 100) if total_events > 0 else 0
        
        # Get today's events
        today = datetime.now().date()
        today_events = [e for e in self.current_week_events if e['date'] == today]
        today_completed = len([e for e in today_events if e['is_completed']])
        today_total = len(today_events)
        
        return {
            'total_events': total_events,
            'completed_events': completed_events,
            'current_events': current_events,
            'upcoming_events': upcoming_events,
            'total_hours': total_hours,
            'completed_hours': completed_hours,
            'completion_percentage': completion_percentage,
            'today_events': today_total,
            'today_completed': today_completed,
            'today_completion': (today_completed / today_total * 100) if today_total > 0 else 0
        }

# Global dashboard instance
dashboard = ProductivityDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/events')
def get_events():
    """API endpoint to get current week events"""
    events = dashboard.get_current_week_events()
    return jsonify(events)

@app.route('/api/stats')
def get_stats():
    """API endpoint to get productivity statistics"""
    stats = dashboard.get_productivity_stats()
    return jsonify(stats)

@app.route('/api/current-event')
def get_current_event():
    """API endpoint to get current event"""
    events = dashboard.get_current_week_events()
    current_event = next((e for e in events if e['is_current']), None)
    return jsonify(current_event)

@app.route('/api/next-event')
def get_next_event():
    """API endpoint to get next upcoming event"""
    events = dashboard.get_current_week_events()
    upcoming_events = [e for e in events if e['is_upcoming']]
    if upcoming_events:
        next_event = min(upcoming_events, key=lambda x: x['start_time'])
        return jsonify(next_event)
    return jsonify(None)

def initialize_dashboard():
    """Initialize the dashboard with Google Calendar authentication"""
    print("🚀 Initializing Productivity Dashboard...")
    
    # Authenticate with Google Calendar
    service = dashboard.authenticate_google_calendar()
    if not service:
        print("❌ Failed to authenticate with Google Calendar")
        return False
    
    print("✅ Successfully authenticated with Google Calendar")
    
    # Get initial events
    events = dashboard.get_current_week_events()
    print(f"📅 Loaded {len(events)} events for current week")
    
    return True

if __name__ == '__main__':
    # Initialize dashboard
    if initialize_dashboard():
        print("🌐 Starting Productivity Dashboard server...")
        print("📱 Open your browser and go to: http://localhost:8080")
        print("🔄 Dashboard will auto-refresh every 30 seconds")
        
        # Start Flask app
        app.run(debug=True, host='0.0.0.0', port=8080)
    else:
        print("❌ Failed to initialize dashboard")
