# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
# Adjust the source path as per your project structure
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000
# Run the Flask app
ENTRYPOINT ["streamlit", "run", "simple_frontend.py", "--server.port=4000", "--server.address=0.0.0.0"]