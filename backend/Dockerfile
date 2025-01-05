FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y procps netcat-openbsd

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Create a user to run the app (not as root)
RUN adduser --disabled-password myuser

# Give the user permission to the /app directory
RUN chown -R myuser:myuser /app

# Switch to root for further actions
USER root

# Copy the wait-for-it.sh script to the container
COPY wait-for-it.sh /usr/local/bin/wait-for-it

# Ensure the script is executable by root user
RUN chmod +x /usr/local/bin/wait-for-it

# Install python3 and pip
RUN apt-get update -y && apt-get install -V -y python3-pip

# Install the Python dependencies including Gunicorn
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Switch back to the regular user for app execution
USER myuser

# Copy the rest of the application files
COPY . .

# Use Gunicorn to run the app, with the wait-for-it script to ensure DB is ready
CMD ["wait-for-it", "db-mysql.cha4akq0c089.us-east-1.rds.amazonaws.com:3306", "--", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

