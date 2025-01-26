FROM python:3.12.2-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY flask_app /app/flask_app

# Set the working directory for Flask to the app directory
WORKDIR /app/flask_app

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]