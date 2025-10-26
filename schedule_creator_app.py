#!/usr/bin/env python3
"""
Schedule Creator Web Application
A comprehensive web UI for creating optimized schedules, Git integration, and Docker deployment
"""

import os
import json
import subprocess
import git
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
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
app.secret_key = 'your-secret-key-change-this'

class ScheduleCreator:
    def __init__(self):
        self.service = None
        self.git_repo = None
        
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
                return None
        
        self.service = build('calendar', 'v3', credentials=creds)
        return self.service
    
    def initialize_git_repo(self):
        """Initialize Git repository"""
        try:
            if not os.path.exists('.git'):
                self.git_repo = git.Repo.init()
                print("✅ Git repository initialized")
            else:
                self.git_repo = git.Repo('.')
                print("✅ Git repository found")
            return True
        except Exception as e:
            print(f"❌ Git initialization failed: {e}")
            return False
    
    def create_optimized_schedule(self, schedule_config):
        """Create optimized schedule based on configuration"""
        
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
    
    def commit_to_git(self, message="Add optimized schedule"):
        """Commit schedule to Git"""
        try:
            if not self.git_repo:
                return False, "Git repository not initialized"
            
            # Add all files
            self.git_repo.git.add('.')
            
            # Commit
            self.git_repo.index.commit(message)
            
            return True, f"Committed: {message}"
            
        except Exception as e:
            return False, f"Git commit failed: {e}"
    
    def push_to_remote(self, remote_name="origin", branch="main"):
        """Push to remote Git repository"""
        try:
            if not self.git_repo:
                return False, "Git repository not initialized"
            
            # Push to remote
            self.git_repo.remotes[remote_name].push(branch)
            
            return True, f"Pushed to {remote_name}/{branch}"
            
        except Exception as e:
            return False, f"Git push failed: {e}"

# Global schedule creator instance
schedule_creator = ScheduleCreator()

@app.route('/')
def index():
    """Main page"""
    return render_template('schedule_creator.html')

@app.route('/api/auth/google')
def auth_google():
    """Authenticate with Google Calendar"""
    try:
        service = schedule_creator.authenticate_google_calendar()
        if service:
            return jsonify({'success': True, 'message': 'Google Calendar authenticated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Google Calendar authentication failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Authentication error: {e}'})

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

@app.route('/api/git/init')
def git_init():
    """Initialize Git repository"""
    try:
        success = schedule_creator.initialize_git_repo()
        if success:
            return jsonify({'success': True, 'message': 'Git repository initialized'})
        else:
            return jsonify({'success': False, 'message': 'Git initialization failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Git init error: {e}'})

@app.route('/api/git/commit', methods=['POST'])
def git_commit():
    """Commit to Git"""
    try:
        data = request.get_json()
        message = data.get('message', 'Add optimized schedule')
        
        success, message_result = schedule_creator.commit_to_git(message)
        return jsonify({'success': success, 'message': message_result})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Git commit error: {e}'})

@app.route('/api/git/push', methods=['POST'])
def git_push():
    """Push to remote Git repository"""
    try:
        data = request.get_json()
        remote = data.get('remote', 'origin')
        branch = data.get('branch', 'main')
        
        success, message = schedule_creator.push_to_remote(remote, branch)
        return jsonify({'success': success, 'message': message})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Git push error: {e}'})

@app.route('/api/docker/build')
def docker_build():
    """Build Docker image"""
    try:
        result = subprocess.run(['docker', 'build', '-t', 'schedule-creator', '.'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Docker image built successfully'})
        else:
            return jsonify({'success': False, 'message': f'Docker build failed: {result.stderr}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Docker build error: {e}'})

@app.route('/api/docker/run', methods=['POST'])
def docker_run():
    """Run Docker container"""
    try:
        data = request.get_json()
        port = data.get('port', '8080')
        
        result = subprocess.run([
            'docker', 'run', '-d', '-p', f'{port}:8080', 
            '--name', 'schedule-creator-app', 'schedule-creator'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return jsonify({'success': True, 'message': f'Docker container running on port {port}'})
        else:
            return jsonify({'success': False, 'message': f'Docker run failed: {result.stderr}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Docker run error: {e}'})

if __name__ == '__main__':
    print("🚀 Starting Schedule Creator Web Application...")
    print("📱 Open your browser and go to: http://localhost:8080")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
