Configuring third-party apps
============================

Aristotle takes care of most of the work of getting a registry setup with the settings import::

    from aristotle_mdr.required_settings import *

but there are few areas for customisation or tweaking.

Django
------

Every django setting can be overridden, but the ones that will be most important are:

* ```DATABASE`` - By default Aristotle will configure a SQLite file-based database.
  While this is fine fors very small low use registries, configuring Django to use a
  fully-fledged relational database management system like PostgreSQL or MySQL will
  be better for larger, high-traffic sites.

* ``ROOT_URLCONF``  'possum_mdr.urls'
* ``WSGI_APPLICATION`` = 'possum_mdr.wsgi.application'


Haystack
--------

For search to work Haystack is required to be installed, there are no options to disable this,
as without search a registry is quite useless. However you can change some settings.

* ``HAYSTACK_SEARCH_RESULTS_PER_PAGE`` - Self explanatory,  this defaults to 10 items per page.
* ``HAYSTACK_CONNECTIONS`` - This define which search indexers are being used and how they are
  connected. By default this uses the `Whoosh Engine <https://pypi.python.org/pypi/Whoosh/>`_,
  which is quite fast and because its a Pure-Python implementation reduces the complexity in getting it setup.
  `For more advanced usage, read the Haystack documentation <http://django-haystack.readthedocs.org/en/latest/tutorial.html#configuration>`_.
* ``HAYSTACK_SIGNAL_PROCESSOR`` - Included for completion, this defaults to ``aristotle_mdr.signals.AristotleSignalProcessor``.
  This is a custom signal processor that performs real-time, status-aware changes to the index. **Read the warnings below for why you probably don't want to change this.**

Warnings about Haystack:
++++++++++++++++++++++++
* Always make sure ``haystack`` is included **once and only once** in ``INSTALLED_APPS``,
  otherwise it will throw errors.
* Make sure ``haystack`` is included in ``INSTALLED_APPS`` *before* ``aristotle_mdr``.
* Be aware that Haystack will only update search indexes when told, Aristotle includes a
  ``SignalProcessor`` that performs registation status-aware real-time updates to the index.
  **Switching this for another processor may expose private information** through search results,
  *but will not allow unauthorised users to access the complete item*.

Grappelli
---------


