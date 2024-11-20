FROM python:3.12-slim

WORKDIR /app

# Copy requirements files
COPY backend/requirements.txt backend-requirements.txt
COPY frontend/requirements.txt frontend-requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r backend-requirements.txt
RUN pip install --no-cache-dir -r frontend-requirements.txt

# Copy the application code
COPY backend /app/backend
COPY frontend /app/frontend

# Create a script to run both services
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000 8501

CMD ["/app/start.sh"]
