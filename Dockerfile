# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json

# Expose port
EXPOSE $PORT

# Run Gunicorn (production server)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

