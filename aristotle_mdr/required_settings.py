import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
FIXTURES_DIRS = [os.path.join(BASE_DIR, 'fixtures')]
STATIC_ROOT =os.path.join(BASE_DIR, "static")

# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# This provides for quick easy set up, but should be changed to a production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'pos.db3'),
    }
}
SECRET_KEY = "OVERRIDE_THIS_IN_PRODUCTION"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Required for admindocs, see: https://code.djangoproject.com/ticket/21386
SITE_ID=None

ALLOWED_HOSTS = []
SOUTH_TESTS_MIGRATE = False

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #added
    'south',
    'inplaceeditform',
    'inplaceeditform_extra_fields',
    'tinymce',

    'bootstrap3',
    'bootstrap3_datetime',
    'reversion', # https://github.com/etianen/django-reversion
    'reversion_compare', # https://github.com/jedie/django-reversion-compare
    'autocomplete_light',
    'notifications',
)

USE_L10N = True
USE_TZ = True
USE_I18N = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.request',
  'aristotle_mdr.context_processors.settings',
)

ROOT_URLCONF = 'aristotle_mdr.urls'
LOGIN_REDIRECT_URL = '/account/home'

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

GRAPPELLI_ADMIN_TITLE = "Aristotle admin interface"
BOOTSTRAP3 = {
    # The Bootstrap base URL
    'base_url': '/static/aristotle_mdr/bootstrap/',
}

# We need this to make sure users can
AUTHENTICATION_BACKENDS = ('aristotle_mdr.backends.AristotleBackend',)

# Used for in place editing
INPLACEEDIT_EDIT_EMPTY_VALUE = 'Double click to edit'
INPLACEEDIT_AUTO_SAVE = False
INPLACEEDIT_EVENT = "dblclick"
INPLACEEDIT_DISABLE_CLICK = True  # For inplace edit text into a link tag
INPLACEEDIT_EDIT_MESSAGE_TRANSLATION = 'Write a translation' # transmeta option
INPLACEEDIT_SUCCESS_TEXT = 'Successfully saved'
INPLACEEDIT_UNSAVED_TEXT = 'You have unsaved changes'
INPLACE_ENABLE_CLASS = 'enable'
DEFAULT_INPLACE_EDIT_OPTIONS = {
'menubar_item':"file",
'auto_height':True,
'auto_width':True,
} # dictionnary of the optionals parameters that the templatetag can receive to change its behavior (see the Advanced usage section)
DEFAULT_INPLACE_EDIT_OPTIONS_ONE_BY_ONE = True # modify the behavior of the DEFAULT_INPLACE_EDIT_OPTIONS usage, if True then it use the default values not specified in your template, if False it uses these options only when the dictionnary is empty (when you do put any options in your template)
#ADAPTOR_INPLACEEDIT_EDIT = 'app_name.perms.MyAdaptorEditInline' # Explain in Permission Adaptor API
#ADAPTOR_INPLACEEDIT = {'myadaptor': 'app_name.fields.MyAdaptor'} # Explain in Adaptor API
INPLACE_GET_FIELD_URL = None # to change the url where django-inplaceedit use to get a field
INPLACE_SAVE_URL = None # to change the url where django-inplaceedit use to save a field
ADAPTOR_INPLACEEDIT_EDIT = 'aristotle_mdr.perms.MyAdaptorEditInline'
ADAPTOR_INPLACEEDIT = {
    'auto_fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
    'auto_m2m': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField',
    'image_thumb': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
    'tiny': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',
    'aristotle': 'aristotle_mdr.fields.AristotleRichTextField',
    'booleanYesNo': 'aristotle_mdr.fields.booleanYesNo',
}

HAYSTACK_SIGNAL_PROCESSOR = 'aristotle_mdr.signals.AristotleSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'INCLUDE_SPELLING':True,
    },
}