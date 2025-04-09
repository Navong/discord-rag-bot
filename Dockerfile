# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file (if you have one) and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

# Copy application files
COPY bot.py .
COPY utils.py .
COPY .env .

# Create directory for PDF storage
RUN mkdir -p ./pdf

# Set environment file
ENV DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV GROQ_API_KEY=${GROQ_API_KEY}

# Run the bot
CMD ["python", "bot.py"]