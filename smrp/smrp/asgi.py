"""
ASGI config for smrp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

# from django.core.asgi import get_asgi_application
from django_asgi_lifespan.asgi import get_asgi_application as get_lifespan_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smrp.settings')

# asgi_app = get_asgi_application()
application = get_lifespan_asgi_application()
