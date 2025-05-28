# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install pip dependencies except torch/torchvision/torchaudio
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install torch, torchvision, torchaudio from PyTorch CPU index
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy the rest of the code
COPY . /app/

# Expose the port FastAPI runs on
EXPOSE 8600

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8600"]
