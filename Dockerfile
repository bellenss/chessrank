# Use the official Python image as a base
FROM python:3.11-slim
# Set the working directory inside the container
WORKDIR /app
# Copy the requirements file first (if exists) to leverage Docker caching
COPY requirements.txt requirements.txt
# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt
# Copy the project files
COPY . .
# Set environment variables
ENV PYTHONUNBUFFERED=1
# Expose the port Django runs on
EXPOSE 8000
# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
