# Base image
# Python 3.8 image from Docker Hub as the base image
FROM python:3.8

# Copy the requirements file into the container and install the required packages
COPY ./requirements.txt /app/requirements.txt

# Set work directory 
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy whole project to docker home directory.
COPY . .

# Expose the port used by the Django application
EXPOSE 8000

CMD ["runserver", "0.0.0.0:8000"]