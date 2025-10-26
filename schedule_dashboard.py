#!/usr/bin/env python3
"""
Work Schedule Dashboard
Shows your clean, organized work schedule
"""

from datetime import datetime, timedelta

def show_schedule_dashboard():
    """Display the work schedule dashboard"""
    
    # Get current date and calculate the week
    today = datetime.now()
    # Find the next Sunday (or current Sunday if today is Sunday)
    days_ahead = 6 - today.weekday()  # Sunday is 6
    if days_ahead == 7:  # If today is Sunday
        days_ahead = 0
    elif days_ahead > 0:  # If we're past Sunday this week
        days_ahead -= 7
    
    sunday = today + timedelta(days=days_ahead)
    
    print("📅 WORK SCHEDULE DASHBOARD")
    print("=" * 80)
    print(f"📆 Week: {sunday.strftime('%B %d')} - {(sunday + timedelta(days=4)).strftime('%B %d, %Y')}")
    print("=" * 80)
    
    # Schedule data
    schedule = [
        # Sunday - Analysis & Planning Day
        {
            'date': sunday,
            'day_name': 'SUNDAY',
            'theme': '📊 ANALYSIS & PLANNING',
            'sessions': [
                {'time': '09:00-10:30', 'title': 'JIRA Analysis - Git Comparison', 'type': '🔍 Analysis'},
                {'time': '10:45-12:15', 'title': 'Test Failure Investigation', 'type': '🔍 Analysis'},
                {'time': '14:00-15:30', 'title': 'Use Case Documentation', 'type': '📝 Documentation'},
                {'time': '15:45-17:15', 'title': 'Implementation Planning', 'type': '📝 Planning'},
            ]
        },
        # Monday - Development Focus Day
        {
            'date': sunday + timedelta(days=1),
            'day_name': 'MONDAY',
            'theme': '🔧 DEVELOPMENT FOCUS',
            'sessions': [
                {'time': '09:00-10:30', 'title': 'Use Case Implementation - Core Logic', 'type': '🔧 Development'},
                {'time': '10:45-12:15', 'title': 'Use Case Implementation - Integration', 'type': '🔧 Development'},
                {'time': '14:00-15:30', 'title': 'Test Environment Setup', 'type': '🔍 Testing'},
                {'time': '15:45-17:15', 'title': 'Integration Test Development', 'type': '🔍 Testing'},
            ]
        },
        # Tuesday - Bootcamp Day
        {
            'date': sunday + timedelta(days=2),
            'day_name': 'TUESDAY',
            'theme': '📚 BOOTCAMP & DEVELOPMENT',
            'sessions': [
                {'time': '08:00-13:00', 'title': 'Bootcamp Session', 'type': '📚 Bootcamp', 'highlight': True},
                {'time': '14:00-15:30', 'title': 'Post-Bootcamp Development', 'type': '🔧 Development'},
                {'time': '15:45-17:15', 'title': 'Testing & Debugging', 'type': '🔍 Testing'},
                {'time': '17:30-19:00', 'title': 'Regular JIRA Tasks', 'type': '🔧 Development'},
            ]
        },
        # Wednesday - Testing & Review Day (Unavailable 4PM-7PM)
        {
            'date': sunday + timedelta(days=3),
            'day_name': 'WEDNESDAY',
            'theme': '🔍 TESTING & REVIEW',
            'sessions': [
                {'time': '09:00-10:30', 'title': 'Comprehensive Testing', 'type': '🔍 Testing'},
                {'time': '10:45-12:15', 'title': 'Bug Fixing Session', 'type': '🔍 Testing'},
                {'time': '13:00-14:30', 'title': 'Final Development Push', 'type': '🔧 Development'},
                {'time': '14:45-15:45', 'title': 'Code Review Preparation', 'type': '🎯 Review', 'note': 'Ends before 4PM unavailability'},
            ]
        },
        # Thursday - Bootcamp Day
        {
            'date': sunday + timedelta(days=4),
            'day_name': 'THURSDAY',
            'theme': '📚 BOOTCAMP & FINALIZATION',
            'sessions': [
                {'time': '08:00-13:00', 'title': 'Bootcamp Session', 'type': '📚 Bootcamp', 'highlight': True},
                {'time': '14:00-15:30', 'title': 'Final Review & Submission', 'type': '🎯 Review'},
                {'time': '15:45-17:15', 'title': 'Documentation Finalization', 'type': '📝 Documentation'},
                {'time': '17:30-19:00', 'title': 'Project Wrap-up', 'type': '🎯 Review'},
            ]
        }
    ]
    
    # Display dashboard
    for day in schedule:
        print(f"\n📅 {day['day_name']}, {day['date'].strftime('%B %d')}")
        print(f"🎯 {day['theme']}")
        print("-" * 60)
        
        for session in day['sessions']:
            highlight = "🌟 " if session.get('highlight') else "   "
            note = f" ({session['note']})" if session.get('note') else ""
            print(f"{highlight}{session['time']} | {session['type']} | {session['title']}{note}")
        
        print()
    
    # Summary
    print("=" * 80)
    print("📊 SCHEDULE SUMMARY")
    print("=" * 80)
    
    total_sessions = sum(len(day['sessions']) for day in schedule)
    bootcamp_hours = 10  # 2 days × 5 hours each
    other_hours = (total_sessions - 2) * 1.5  # 2 bootcamp sessions, rest are 1.5h each
    
    print(f"📈 Total Sessions: {total_sessions}")
    print(f"⏰ Total Hours: {bootcamp_hours + other_hours:.1f} hours")
    print(f"📚 Bootcamp Hours: {bootcamp_hours} hours")
    print(f"🔧 Work Hours: {other_hours:.1f} hours")
    
    print(f"\n📋 Calendar Organization:")
    print(f"  🔧 Development Work - Coding and implementation")
    print(f"  📚 Bootcamp Sessions - Organization training")
    print(f"  🔍 Analysis & Testing - Testing and debugging")
    print(f"  📝 Documentation & Planning - Planning and docs")
    print(f"  🎯 Review & Submission - Reviews and submissions")
    
    print(f"\n💡 Tips:")
    print(f"  • Check Google Calendar for your clean, organized schedule")
    print(f"  • Bootcamp sessions are organization-wide (8 AM - 1 PM)")
    print(f"  • Other sessions are 1.5 hours for better focus")
    print(f"  • Each calendar can be toggled on/off independently")
    print(f"  • Smart reminders: 1 day email + 15 min popup")

if __name__ == '__main__':
    show_schedule_dashboard()
