# Build: docker build -t backend-server .
# Run: docker run -d -p 6000:6000 --name backend-server backend-server
# Stop: docker stop backend-server

#Base image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt requirements.txt

# Installthe requird packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Install required libraries for OpenCV
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt update

# Install required libraries for PyTorch
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6

# Install wget
RUN apt install wget -y

# Create the directory for the model
RUN mkdir -p /root/.deepface/weights

RUN cd /root/.deepface/weights

# Download the model
RUN wget https://github.com/serengil/deepface_models/releases/download/v1.0/facenet_weights.h5

# Install FLASK_CORS
RUN pip install flask_cors

# Execute the command to start the server
CMD ["gunicorn", "--bind", "0.0.0.0:6000", "wsgi:app"]

EXPOSE 6000
