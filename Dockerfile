# Base image
FROM python:3.10

# Expose ports
EXPOSE 5000

# Update system and install gunicorn
RUN apt update -y
RUN apt upgrade -y
RUN pip install --upgrade pip
RUN pip install gunicorn

# Create and use project directory
WORKDIR /app

# Copy and install requirements
ADD requirements.txt .
RUN pip install -r requirements.txt

# Copy source files
ADD src .

# Entrypoin
ENTRYPOINT gunicorn --bind :5000 app:app
