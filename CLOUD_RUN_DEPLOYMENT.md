# Cloud Run Deployment Guide for Calendar Scheduler

## 🚀 Deploy to Google Cloud Run (Modern Alternative)

### Option 1: Enable Billing for App Engine
1. **Go to**: https://console.cloud.google.com/billing/linkedaccount?project=calendar-scheduler-1761455862
2. **Link billing account** to your project
3. **Continue with App Engine** deployment

### Option 2: Deploy to Cloud Run (Recommended - No Billing Required for Free Tier)

#### Step 1: Enable Cloud Run API
```bash
gcloud services enable run.googleapis.com
```

#### Step 2: Build and Deploy
```bash
# Build container
gcloud builds submit --tag gcr.io/calendar-scheduler-1761455862/calendar-scheduler

# Deploy to Cloud Run
gcloud run deploy calendar-scheduler \
  --image gcr.io/calendar-scheduler-1761455862/calendar-scheduler \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

#### Step 3: Get Your URL
```bash
# Get the service URL
gcloud run services describe calendar-scheduler --region=us-central1 --format="value(status.url)"
```

### Benefits of Cloud Run:
- ✅ **No billing required** for free tier (2 million requests/month)
- ✅ **Pay per use** - only pay when requests are processed
- ✅ **Modern containerized** deployment
- ✅ **Auto-scaling** from 0 to 1000 instances
- ✅ **Global CDN** and edge caching
- ✅ **HTTPS** enabled by default

### Your App Features:
- 🧠 **NLP Processing**: Natural language schedule creation
- 📅 **Smart Pickers**: Modern date/time inputs
- 🎨 **Netflix UI**: Dark theme with animations
- 📱 **Mobile Ready**: Responsive design
- 🔄 **Real-time**: Instant AI processing
- 📊 **Event Management**: Dynamic event handling

### Cost Comparison:
- **App Engine**: Requires billing account, $0.05/hour minimum
- **Cloud Run**: Free tier available, pay per request only

## 🎯 Quick Cloud Run Deploy:
```bash
# One command deployment
gcloud run deploy calendar-scheduler \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Your Interactive AI Schedule Creator will be live! 🚀
