"""Configurarea ASGI pentru pornirea aplicatiei pe un server compatibil."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brunch_project.settings')

application = get_asgi_application()
