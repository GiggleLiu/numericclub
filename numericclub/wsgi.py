"""
WSGI config for numericclub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys 

with open('/home/leo/website/numericclub/numericclub/wsgi.log', 'w') as f:
    f.write('%s'%sys.executable)
sys.path.append('/home/leo/website/numericclub') 
 
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "numericclub.settings")

application = get_wsgi_application()
