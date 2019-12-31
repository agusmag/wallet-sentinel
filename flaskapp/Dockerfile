# Use the Python:3.7.6 container image
FROM python:3.7.6-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Set the locale in the container
RUN apt-get clean && apt-get update && apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN dpkg-reconfigure locales

# Install All the Flask App dependencies
RUN pip install -r requirements.txt

# Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]