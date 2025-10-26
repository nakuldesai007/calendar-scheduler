# 📅 Google Calendar Work Scheduler

Creates clean, organized work schedules with specialized calendars.

## 🎯 Essential Scripts

### 🚀 `fresh_schedule_creator.py`
**Main script** - Creates a clean work schedule with:
- 5 specialized calendars (Development, Bootcamp, Analysis, Documentation, Review)
- Respects organization-wide bootcamp timing (8 AM - 1 PM)
- Focused 1.5-hour work sessions
- Clear separation of work types

### 📊 `schedule_dashboard.py`
**Visual dashboard** - Shows your schedule in an easy-to-read format:
- Week overview with all sessions
- Color-coded work types
- Time summaries and statistics
- Quick reference for daily planning

## 🚀 Quick Start

1. **Setup**: Follow `setup_instructions.md`
2. **Create Schedule**: `python fresh_schedule_creator.py`
3. **View Dashboard**: `python schedule_dashboard.py`

## 📅 Schedule Overview

### **Sunday** - Analysis & Planning
- 9:00-10:30 AM: JIRA Analysis - Git Comparison
- 10:45-12:15 PM: Test Failure Investigation
- 2:00-3:30 PM: Use Case Documentation
- 3:45-5:15 PM: Implementation Planning

### **Monday** - Development Focus
- 9:00-10:30 AM: Use Case Implementation - Core Logic
- 10:45-12:15 PM: Use Case Implementation - Integration
- 2:00-3:30 PM: Test Environment Setup
- 3:45-5:15 PM: Integration Test Development

### **Tuesday** - Bootcamp & Development
- 8:00 AM-1:00 PM: **Bootcamp Session** (Organization-wide)
- 2:00-3:30 PM: Post-Bootcamp Development
- 3:45-5:15 PM: Testing & Debugging
- 5:30-7:00 PM: Regular JIRA Tasks

### **Wednesday** - Testing & Review
- 9:00-10:30 AM: Comprehensive Testing
- 10:45-12:15 PM: Bug Fixing Session
- 2:00-3:30 PM: Final Development Push
- 3:45-5:15 PM: Code Review Preparation

### **Thursday** - Bootcamp & Finalization
- 8:00 AM-1:00 PM: **Bootcamp Session** (Organization-wide)
- 2:00-3:30 PM: Final Review & Submission
- 3:45-5:15 PM: Documentation Finalization
- 5:30-7:00 PM: Project Wrap-up

## 🎯 Key Features

- ✅ Clean, organized calendars
- ✅ Respects bootcamp organization schedule
- ✅ Focused work sessions (1.5 hours)
- ✅ 5 specialized calendars for organization
- ✅ Visual dashboard for easy viewing
- ✅ Smart reminders (1 day + 15 min before)

## 📁 Project Structure

```
calendar-scheduler/
├── fresh_schedule_creator.py    # Main script
├── schedule_dashboard.py        # Visual dashboard
├── requirements.txt             # Dependencies
├── setup_instructions.md        # Setup guide
├── credentials.json             # Google API credentials
└── token.pickle                 # Authentication token
```

## 🔧 Troubleshooting

- **Authentication errors**: Delete `token.pickle` and run again
- **Missing credentials**: Ensure `credentials.json` is in the correct location
- **API errors**: Verify Google Calendar API is enabled

---

**Happy Scheduling! 🎉**