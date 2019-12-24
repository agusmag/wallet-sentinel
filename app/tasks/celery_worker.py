from app import create_app

# Set Celery Config to use the same Flask App Environment
app = create_app()
app.app_context().push()

from tasks import celery