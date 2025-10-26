# Use Cloud Run instead of App Engine for modern deployment
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements-gcp.txt .
RUN pip install --no-cache-dir -r requirements-gcp.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]