# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "run_app.py"]
