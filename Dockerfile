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

# Run the application - Railway will use its own startCommand
CMD ["python", "-c", "print('Container ready')"]