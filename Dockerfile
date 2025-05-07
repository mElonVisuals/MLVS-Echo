# Use official Python image
FROM python:3.10-slim

# Install FFmpeg (essential for music bots)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run the bot
CMD ["python", "bot.py"]
