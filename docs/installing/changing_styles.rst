Changing the look and feel of the site
======================================

Changing site CSS using Django ``staticfiles``
----------------------------------------------

Changing the CSS of the site can be done by overriding the static files that serve the
Bootstrap and Aristotle CSS files, these are available at::

    aristotle_mdr/static/aristotle_mdr/css/aristotle.css
    aristotle_mdr/static/aristotle_mdr/bootstrap/bootstrap.min.css

Overriding these will require setting the ``STATICFILES_DIR`` setting in ``settings.py`` , like so::

    STATICFILES_DIR = [os.path.join(BASE_DIR, "site_static")]

Its important, to make sure if setting a ``STATICFILES_DIR`` that
``'django.contrib.staticfiles.finders.FileSystemFinder'`` is added to
the ``STATICFILES_FINDERS`` setting. If importing all of the settings from
Aristotles `required_settings.py` file this is already included, so this doesn't need
to be redefined. But if ``settings.py`` doesn't import ``required_settings.py``,
``STATICFILES_FINDERS`` can be declared like this::

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

Once this is set, to override the Aristotle bootstrap css, a file at the
following location in the project site will be used instead::

    custom_site_static/aristotle_mdr/bootstrap/bootstrap.min.css

More information about these is available in the
`Django documentation on static files <https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/#staticfiles-finders>`_.


Changing the Bootstrap file by overriding the settings
------------------------------------------------------

Aristotle uses `Django-bootstrap3 <https://github.com/dyve/django-bootstrap3>`_ to
import bootstrap. By default Aristotle stores the boostrap file at::

but, an alternative solution is to override this value be redefining the `BOOTSTRAP3` setting
in your projects ``settings.py``, like so::

    BOOTSTRAP3 = {
        # The Bootstrap base URL
        'base_url': '/static/your_path_to/bootstrap/',
    }

Completely overhauling the site
-------------------------------

It is also possbile to override the home page and base templates to completely overhaul
the look and feel of the site, and these are available under the ``templates`` directory at:

*  ``aristotle_mdr/templates/aristotle_mdr/base.html``
*  ``aristotle_mdr/templates/aristotle_mdr/static/home.html``

However, doing so may break the rendering of pages and prevent the registry from working.
It is strongly recommended that overrides of these files are done by someone with
a strong working knowledge of HTML, CSS and Django templates.