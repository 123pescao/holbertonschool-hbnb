# Use Alpine Linux as the base image with Python
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variable for the application port
ENV FLASK_RUN_PORT=5000

# Command to run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
