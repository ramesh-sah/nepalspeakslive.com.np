FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install dependencies

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make port 8000 available
EXPOSE 8003

# Run collectstatic on build
# RUN python manage.py collectstatic --noinput

# Start Gunicorn
CMD ["gunicorn", "mount_everest_summit.wsgi:application", "--bind", "0.0.0.0:8003"]
