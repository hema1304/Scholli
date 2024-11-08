# Use the official Python image as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock (if available) to the container
COPY Pipfile* ./

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install dependencies from Pipfile
RUN pipenv install --system --deploy

# Copy the rest of the application code to the container
COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=./app.py

# Expose port 80 (or the port your Flask app runs on)
EXPOSE 80

# Run the Flask application in debug mode using pipenv
CMD ["pipenv", "run", "flask", "--debug", "run", "-h", "0.0.0.0"]
