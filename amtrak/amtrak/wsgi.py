"""
WSGI config for amtrak project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

# DO NOT TOUCH THIS FILE AT ALL. NOTHING TO DO HERE !


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amtrak.settings")

application = get_wsgi_application()
