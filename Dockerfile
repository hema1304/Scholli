# Use the official Python image as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 80 (or the port your Flask app runs on)
EXPOSE 80

# Set environment variables (if required)
# ENV FLASK_ENV=production

# Run the Flask application
CMD ["python", "app.py"]  # Change app.py to your main Python file if named differently
