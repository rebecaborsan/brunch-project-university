"""Configurarea WSGI pentru pornirea aplicatiei pe un server compatibil."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brunch_project.settings')

application = get_wsgi_application()
