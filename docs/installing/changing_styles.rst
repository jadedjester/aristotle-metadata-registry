Changing the look and feel of the site
======================================

Changing site CSS
-----------------

Changing the CSS of the site can be done by overriding the static files that serve the
Bootstrap and Aristotle CSS files, these are available at:

*  ``aristotle_mdr/base.html``
*  ``aristotle_mdr/static/home.html``

Overriding these will require setting the ``STATICFILES_DIR`` setting and ensuring that
``'django.contrib.staticfiles.finders.FileSystemFinder'`` is added to the ``STATICFILES_FINDERS``.
More information about these is available in the
`Django documentation on static files <https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/#staticfiles-finders>`_.

Completely overhauling the site
-------------------------------

It is also possbile to override the home page and base templates to completely overhaul
the look and feel of the site, and these are available under the ``templates`` directory at:

*  ``aristotle_mdr/base.html``
*  ``aristotle_mdr/static/home.html``

However, doing so may break the rendering of pages and pervent the registry from working.
It is strongly recommended that overrides of these files are done by someone with
a strong working knowledge of HTML, CSS and Django templates.