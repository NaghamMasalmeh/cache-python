# Base image
FROM python:3.8

# Copy the requirements file into the container and install the required packages
COPY ./requirements.txt /app/requirements.txt

# Set work directory 
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy whole project to docker home directory.
COPY . .

# Set environment variables
ENV MONGO_HOST localhost
ENV MONGO_PORT 27017

# Expose the port used by the Django application
EXPOSE 8000

CMD ["runserver", "0.0.0.0:8000"]