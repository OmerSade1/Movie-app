FROM python:3.9-slim
LABEL authors="BiomedicLJZ"

RUN apt-get update && apt-get install -y procps

WORKDIR /app

COPY requirements.txt  requirements.txt

# Create a user to run the app not as root
RUN adduser --disabled-password myuser

# Give the user permission to the /app directory
RUN chown -R myuser:myuser /app

# Switch to the new user
USER myuser

# give the user permission to the execute the app
RUN chmod +x /app

USER root
#Install python3
RUN apt-get update -y && apt-get install -V -y python3-pip

# Install requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

USER myuser

COPY . .

CMD ["python3", "app.py"]