import os
from aristotle_mdr.required_settings import *

SECRET_KEY = 'inara+vtkprm7@0(fsc$+grbz9-s+tmo9d)e#k(9uf8m281&$7xhdkjr'
#SOUTH_TESTS_MIGRATE = False
#SKIP_SOUTH_TESTS = True

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

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'aristotle_mdr/tests/whoosh_index'),
        'INCLUDE_SPELLING':True,
    },
}

# https://docs.djangoproject.com/en/1.6/topics/testing/overview/#speeding-up-the-tests
# We do a lot of user log in testing, this should speed stuff up.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
