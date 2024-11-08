# Use the official Python image as a base image
FROM python:3.10

WORKDIR /app


COPY . .

# Install dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port Flask will run on
EXPOSE 5000

# Run the application using Flask's built-in server
CMD ["flask", "run"]
