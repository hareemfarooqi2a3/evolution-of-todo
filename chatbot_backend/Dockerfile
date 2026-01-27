# Use a lightweight Python base image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY chatbot_backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire chatbot_backend application code
COPY chatbot_backend/ .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
