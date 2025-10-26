# Google Cloud Deployment Guide for Calendar Scheduler

## 🚀 Deploy Your Interactive AI Schedule Creator to Google Cloud

### Prerequisites
- Google Cloud Platform account
- Google Cloud SDK installed
- Project with billing enabled

### Step 1: Install Google Cloud SDK
```bash
# macOS
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

### Step 2: Initialize Google Cloud
```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create calendar-scheduler-app --name="Calendar Scheduler"

# Set the project
gcloud config set project calendar-scheduler-app

# Enable App Engine
gcloud app create --region=us-central
```

### Step 3: Deploy to App Engine
```bash
# Deploy your app
gcloud app deploy

# View your app
gcloud app browse
```

### Step 4: Configure Environment Variables
In Google Cloud Console:
1. Go to App Engine → Settings → Environment Variables
2. Add:
   - `FLASK_ENV=production`
   - `FLASK_DEBUG=false`

### Step 5: Set up Google Calendar API
1. Go to Google Cloud Console → APIs & Services → Credentials
2. Create OAuth 2.0 Client ID
3. Add your App Engine URL to authorized redirect URIs
4. Download credentials.json and upload to App Engine

### Your App Will Be Available At:
- **App Engine URL**: `https://calendar-scheduler-app.appspot.com`
- **Custom Domain**: Configure in App Engine settings

### Features Included:
- 🧠 NLP-powered schedule creation
- 📅 Smart date/time pickers
- 🎨 Netflix-inspired dark theme UI
- 📱 Mobile-responsive design
- 🔄 Real-time AI processing
- 📊 Dynamic event management
- 🌐 Google Cloud hosting

### Cost:
- **Free Tier**: 28 frontend instance hours/day
- **Paid**: $0.05/hour per instance after free tier
- **Storage**: $0.026/GB/month

### Monitoring:
- View logs: `gcloud app logs tail`
- Monitor performance in Google Cloud Console
- Set up alerts for errors or performance issues

## 🎯 Quick Deploy Commands:
```bash
# One-time setup
gcloud auth login
gcloud projects create calendar-scheduler-app
gcloud config set project calendar-scheduler-app
gcloud app create --region=us-central

# Deploy
gcloud app deploy
gcloud app browse
```

Your Interactive AI Schedule Creator will be live on Google Cloud! 🚀
