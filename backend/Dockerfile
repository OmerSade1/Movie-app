FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y procps

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Create a user to run the app (not as root)
RUN adduser --disabled-password myuser

# Give the user permission to the /app directory
RUN chown -R myuser:myuser /app

# Switch to the new user
USER myuser

# Give the user permission to execute the app
RUN chmod +x /app

# Switch to root for installing dependencies
USER root

# Install python3 and pip
RUN apt-get update -y && apt-get install -V -y python3-pip

# Install the Python dependencies including Gunicorn
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Switch back to the regular user
USER myuser

# Copy the rest of the application files
COPY . .

# Use Gunicorn to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
