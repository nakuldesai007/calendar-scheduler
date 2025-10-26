# Google Calendar API Setup Instructions

## Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "Calendar Scheduler"
4. Click "Create"

## Step 2: Enable Google Calendar API
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

## Step 3: Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in required fields (App name, User support email, Developer email)
   - Add your email to test users
4. For Application type, choose "Desktop application"
5. Give it a name like "Calendar Scheduler Desktop"
6. Click "Create"
7. Download the JSON file and rename it to `credentials.json`
8. Place `credentials.json` in this directory

## Step 4: Run the Calendar Scheduler
Once you have `credentials.json` in place, run:
```bash
source venv/bin/activate
python calendar_scheduler.py
```

The first time you run it, it will open a browser window for authentication.
After authentication, it will create a `token.pickle` file for future runs.

## What the Script Does
The script creates a detailed work schedule for the week including:
- **Sunday**: JIRA analysis and use case documentation
- **Monday**: Implementation and integration testing setup
- **Tuesday**: Bootcamp session + development work
- **Wednesday**: Final development push and review
- **Thursday**: Bootcamp session + wrap-up

All events will be added to your primary Google Calendar with proper descriptions and reminders.
