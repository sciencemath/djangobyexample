"""
if we don't want to pass --settings:
`python manage.py runserver --settings=educa.settings.local`
then we can define an evironment variable:
`export DJANGO_SETTINGS_MODULE=educa.settings.local` 
"""
from .base import *

DEBUG = True

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}