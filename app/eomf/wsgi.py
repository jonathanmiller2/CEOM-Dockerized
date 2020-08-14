# import os, sys

# sys.path.append('/web/eomf/prod/eomf/')
# sys.path.append('/web/eomf/prod/')
# sys.path.append('/web/eomf/lib/')
# os.environ['MPLCONFIGDIR'] = '/var/www/.matplotlib'
# os.environ['DJANGO_SETTINGS_MODULE'] = 'eomf.settings'
# os.environ["CELERY_LOADER"] = "django"

# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eomf.settings')

application = get_wsgi_application()