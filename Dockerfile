# Use Cloud Run instead of App Engine for modern deployment
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application with gunicorn
# Use $PORT env variable or default to 8080
CMD gunicorn --bind "0.0.0.0:${PORT:-8080}" schedule_creator_app:app