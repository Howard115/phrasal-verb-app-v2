#!/bin/bash

# Start the backend service
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start the frontend service
cd /app/frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
