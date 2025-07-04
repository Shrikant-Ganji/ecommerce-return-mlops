# deployment/Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 80

# Run the API
CMD ["uvicorn", "deployment.app:app", "--host", "0.0.0.0", "--port", "80"]
