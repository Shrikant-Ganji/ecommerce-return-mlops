# Dockerfile (in root folder)

FROM python:3.11-slim

# Set working directory to app root
WORKDIR /app

# Copy everything from your local project to container
COPY . .

# Install dependencies from root
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 80

# Run FastAPI app (now deployment is a module because of __init__.py)
CMD ["uvicorn", "deployment.app:app", "--host", "0.0.0.0", "--port", "80"]
