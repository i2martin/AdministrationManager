# Use the official Python image as the base image
FROM python:3.9


# Install the application dependencies
RUN pip install -r requirements.txt

# Define the entry point for the container
CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "app:app"]