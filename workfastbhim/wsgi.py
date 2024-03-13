"""
WSGI config for workfastbhim project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add the path to the parent directory of workfastbhim to Python path
sys.path.append('/root')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workfastbhim.settings')

application = get_wsgi_application()
