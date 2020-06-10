"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from .default_settings import *

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOGLEVEL,
            'class': 'logging.FileHandler',
            'filename': './{}.log'.format(LOGLEVEL),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOGLEVEL,
            'propagate': True,
        },
    },
}

AUTHORIZATION = {
    "base_path": "http://auth",
    "verify_api": "/validation",
    "port": 8001,
}