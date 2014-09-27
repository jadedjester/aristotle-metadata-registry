import os
from aristotle_mdr.required_settings import *

project_dir = os.path.abspath('../') # or path to the dir. that the db should be in.
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
   }
}
INSTALLED_APPS = (
    #The good stuff
    'haystack',
    'aristotle_mdr',
) + INSTALLED_APPS
