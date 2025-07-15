import os
from django.core.wsgi import get_wsgi_application
from werkzeug.serving import run_simple

# Point to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = get_wsgi_application()

if __name__ == "__main__":
    run_simple('0.0.0.0', 8000, app)
