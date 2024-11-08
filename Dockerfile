# Use the official Python image as a base image
FROM python:3.10

WORKDIR /app


COPY . .

# Install dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app files

# Expose port
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Expose port 80 (or the port your Flask app runs on)
CMD ["gunicorn", "application:app", "-b", "0.0.0.0:5000", "-w", "4"]
