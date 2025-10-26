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

# Railway will use startCommand from railway.toml
CMD ["echo", "Use Railway startCommand"]