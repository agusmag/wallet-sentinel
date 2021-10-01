# Use the Python:3.7.6 container image
FROM python:3.7.6-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Set the locale in the container
RUN apt-get clean && apt-get update && apt-get install -y locales && locale-gen es_AR.UTF-8
ENV LANG es_AR.UTF-8
ENV LANGUAGE es_AR:en
ENV LC_ALL es_AR.UTF-8
RUN dpkg-reconfigure locales

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install All the Flask App dependencies
RUN pip install -r requirements.txt

# Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]