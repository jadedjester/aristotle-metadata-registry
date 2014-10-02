import os
from aristotle_mdr.required_settings import *

project_dir = os.path.abspath('../') # or path to the dir. that the db should be in.
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

# https://docs.djangoproject.com/en/1.6/topics/testing/overview/#speeding-up-the-tests
# We do a lot of user log in testing, this should speed stuff up.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)