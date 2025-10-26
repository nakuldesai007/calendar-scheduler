# 📅 Google Calendar Work Scheduler

A Python script that automatically creates a detailed work schedule in your Google Calendar, designed for busy professionals with multiple commitments including bootcamp sessions.

## 🎯 Features

- **Automated Schedule Creation**: Creates a complete 5-day work schedule (Sunday-Thursday)
- **Bootcamp Integration**: Properly schedules bootcamp sessions (Tuesday & Thursday 8AM-1PM)
- **Detailed Task Blocks**: Includes specific time blocks for:
  - Carried over JIRA work (git comparison, test analysis)
  - Use case analysis and implementation
  - Integration testing
  - Regular JIRA work
  - Review and submission tasks
- **Smart Reminders**: Email and popup notifications (1 day + 30 min before)
- **Timezone Support**: Configurable timezone handling
- **Google Calendar Integration**: Direct API integration with your Google Calendar

## 📋 Prerequisites

- Python 3.6+
- Google Cloud Project with Calendar API enabled
- Google Calendar API credentials

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd calendar-scheduler
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

### 4. Create Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Download the JSON file and rename it to `credentials.json`
5. Place `credentials.json` in the project directory

### 5. Run the Script
```bash
python calendar_scheduler.py
```

### 6. First Run Authentication
- The script will open your browser
- Sign in to your Google account
- Grant permissions to access your calendar
- The script will create a `token.pickle` file for future runs

## 📅 Schedule Overview

### **Sunday** (9AM-6PM)
- **9AM-1PM**: Carried Over JIRA - Git Comparison & Test Analysis
- **2PM-6PM**: Use Case Analysis & Documentation

### **Monday** (9AM-6PM)  
- **9AM-1PM**: Use Case Implementation
- **2PM-6PM**: Integration Testing Setup

### **Tuesday**
- **8AM-1PM**: Bootcamp Session
- **2PM-7PM**: Development & Testing

### **Wednesday** (9AM-6PM)
- **9AM-1PM**: Final Development Push  
- **2PM-6PM**: Review & Submission

### **Thursday**
- **8AM-1PM**: Bootcamp Session
- **2PM-7PM**: Wrap-up & Documentation

**Total work time: 34 hours** across 5 days, perfectly balanced with bootcamp schedule!

## ⚙️ Customization

You can modify the schedule by editing the `schedule` list in the `create_work_schedule()` function:

```python
schedule = [
    {
        'date': sunday,
        'events': [
            {
                'title': 'Your Custom Task',
                'start': '09:00',
                'end': '13:00',
                'description': 'Detailed description of the task',
                'location': 'Optional location'
            }
        ]
    }
]
```

### Configuration Options:
- **Times**: Modify 'start' and 'end' values (24-hour format)
- **Descriptions**: Update task descriptions
- **Locations**: Add specific locations
- **Timezone**: Adjust timezone in `create_calendar_event()` function

## 🔧 Troubleshooting

### Common Issues:
- **Authentication errors**: Delete `token.pickle` and run again
- **Missing credentials**: Ensure `credentials.json` is in the correct location
- **API errors**: Verify Google Calendar API is enabled in your project
- **Permission errors**: Check that OAuth scopes include calendar access

### Debug Mode:
Add print statements to track the authentication flow:
```python
print(f"Creating event: {title} from {start_time} to {end_time}")
```

## 📁 Project Structure

```
calendar-scheduler/
├── calendar_scheduler.py    # Main script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── credentials.json        # Google API credentials (you provide)
└── token.pickle           # Authentication token (auto-generated)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Calendar API for seamless integration
- Python community for excellent libraries
- All contributors who help improve this tool

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the Google Calendar API documentation
3. Open an issue in this repository

---

**Happy Scheduling! 🎉**
