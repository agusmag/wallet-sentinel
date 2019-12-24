FROM python:3.7.6-stretch

ADD . /flask-app

WORKDIR /flask-app

# Install All the Flask App dependencies
RUN pip install -r requirements.txt

RUN pip install gunicorn[gevent]

EXPOSE 5000

# Set the container's default startup command to a Gunicorn call
# The worker class is gevent -> lightweight concurrency lib for cooperative multitasking
# Numbers of workers should equal to an number of cores on the server
CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
