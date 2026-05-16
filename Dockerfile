# Base Python Image
FROM python:3.11-slim

# Set Working Directory
WORKDIR /app

# Copy Requirements File
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Project Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Complete Project
COPY . .

# Expose Flask Port
EXPOSE 7860

# Run Flask Application
CMD ["python", "app.py"]