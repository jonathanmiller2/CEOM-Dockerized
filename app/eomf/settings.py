# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy
# Django settings for eomf project.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(__file__)

DEBUG = int(os.environ.get("DJANGO_DEBUG", default=0))

#TODO: Remove eomf-dev1 if development environment changes off the VM I'm using right now
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

ADMINS = [
    ('Jonathan', 'jonathan.g.miller@ou.edu'),
]


DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE", default="django.contrib.gis.db.backends.postgis"),
        'HOST': os.environ.get("SQL_HOST", default="db"),
        'NAME': os.environ.get("SQL_DATABASE", default="eomf"),
        'USER': os.environ.get("SQL_USER", default="eomf"),
        'PASSWORD': os.environ.get("SQL_PASSWORD", default="password"),
        "PORT": os.environ.get("SQL_PORT", "5432")
    },
}

#WARNING: THIS MIGHT NEED TO BE UNCOMMENTED IF GEOS ERRORS OCCUR
#THIS IS A NOTE TO FUTURE JONATHAN
#IF YOU SEE THIS I FORGOT ABOUT IT, WHICH IS NOT GOOD
#GEOS_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/libgeos_c.so'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
#LANGUAGE_CODE = 'es-ES'
LANGUAGES = ( 
    ('en', format_lazy('{}{}{}', 'English (', _('English'), ')')),
    ('zh-cn',format_lazy('{}{}{}', '中国简化 (',_('Chinese'),')')),
    ('es', format_lazy('{}{}{}', 'Español (',_('Spanish'),')')),
    ('ne', format_lazy('{}{}{}', 'नेपाली (',_('Nepali'),')')),
    ('fr', format_lazy('{}{}{}', 'Français(',_('French'),')')),
)

LOCALE_PATHS = (
     os.path.join(BASE_DIR,'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
#USE_L10N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

#File permissions for uploaded media
FILE_UPLOAD_PERMISSIONS = 0o644

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/admin/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")
STATIC_URL = '/static/'

# Additional locations of static files
#STATICFILES_DIRS = (
#    os.path.join(os.path.dirname(__file__), "static_common/"),
#)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']


MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'eomf.middleware.KMLMiddleware',
)
#MIDDLEWARE_CLASSES = (
#   'django.middleware.common.CommonMiddleware',
#   'django.contrib.sessions.middleware.SessionMiddleware',
#   'django.middleware.csrf.CsrfViewMiddleware',
#   'django.contrib.auth.middleware.AuthenticationMiddleware',
#   'django.middleware.locale.LocaleMiddleware',
#   'django.contrib.messages.middleware.MessageMiddleware',
#   'eomf.pages.middleware.ContentpageFallbackMiddleware',
#   'eomf.middleware.KMLMiddleware',
#)

ROOT_URLCONF = 'eomf.urls'
WSGI_APPLICATION = 'eomf.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), "templates/"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors' : [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


INSTALLED_APPS = [

    'grappelli', # Better admin interface

    'filebrowser', 
    'sorl.thumbnail', # Picture thumbnails
    'captcha', # Captcha for forms

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.flatpages',
    
    'django_countries',
    'django_extensions', #Needed to nuke/recreate the database

    'autotranslate',
    'chunked_upload',
    #'localflavor',
    'phonenumber_field',

    'eomf.accounts',
    'eomf.photos',
    'eomf.publications',
    'eomf.inventory',
    'eomf.visualization',
    'eomf.geohealth',
    'eomf.pages',
    'eomf.birds',
    'eomf.h5n1',
    'eomf.gisday',
    'eomf.projects',
    'eomf.aboutus',
    'eomf.workshops',
    'eomf.stats',
    'eomf.feedback',
    'eomf.towers',
    'eomf.eomfshare',
    'eomf.maps',
    'eomf.water',
    #'aoitest',
    #'poi',

    
    #'olwidget',
    'tinymce', #Cool Text editor
    'crispy_forms', # Cool forms rendered
    #TODO: Remove all references to crispy forms. Unnescessary dependency. 


]

AUTH_PROFILE_MODULE = 'accounts.Profile'

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "advimage,advlink,fullscreen,visualchars,paste,media,template,searchreplace,table",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_buttons1': "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
    'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,forecolor,backcolor",
    'theme_advanced_buttons3': "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,fullscreen",
    'theme_advanced_buttons4': "",
    'dialog_type': "modal",
    'theme': "advanced",
    'remove_script_host': False,
    'convert_urls': False,
    #'cleanup_on_startup': True,
    #"width": "100%",
    "height": "800px",
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = False

TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = True
TINYMCE_FILEBROWSER = True

GRAPPELLI_ADMIN_TITLE = "EOMF Administration Site"

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'filters': {
       'require_debug_false': {
           '()': 'django.utils.log.RequireDebugFalse'
       }
   },
   'handlers': {
       'mail_admins': {
           'level': 'ERROR',
           'filters': ['require_debug_false'],
           'class': 'django.utils.log.AdminEmailHandler'
       }
   },
   'loggers': {
       'django.request': {
           'handlers': ['mail_admins'],
           'level': 'ERROR',
           'propagate': True,
       },
   }
}
#ALLOWED_HOSTS = [*] 
#BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_USER = "guest"
#BROKER_PASSWORD = "guest"
#BROKER_VHOST = "/"
#THUMBNAIL_DEBUG=True
THUMBNAIL_DEBUG = True
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.OAuth2Authentication',
#     ),
# }


CACHES = {
    'default': {
        'BACKEND':
        'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#Rosetta preferences

ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'
ROSETTA_GOOGLE_TRANSLATE=True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS=True
ROSETTA_WSGI_AUTO_RELOAD =True
#ROSETTA_UWSGI_AUTO_RELOAD=True
ROSETTA_MESSAGES_PER_PAGE= 50

# DBGETTEXT OPTS TO TRANSLATE MODELS
DBGETTEXT_PROJECT_OPTIONS = 'eomf.dbgettext_options'
DBGETTEXT_PATH='dbgettext_files'
DBGETTEXT_SPLIT_SENTENCES=False
FEEDBACK_EMAIL = "jonathan.g.miller@ou.edu;jonathanmiller2@hotmail.com"

#Celery
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

#TODO: Change the http to https
#CORS_ALLOWED_ORIGINS = ["http://"+x for x in os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")]
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS = ["http://eomf-dev1.sooner.net.ou.edu"]