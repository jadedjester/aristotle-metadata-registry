Aristotle Settings required in Django-settings
==============================================

``ARISTOTLE_SETTINGS``
----------------------

The following are required within a dictionary in the settings for the configured Django project.

* ``SITE_NAME`` - The main title for the site - required format ``string`` or ``unicode``
* ``SITE_BRAND`` - A URL to the logo to use for the site, this can be relative or absolute.
* ``SITE_INTRO`` - The introductory text use on the home page as a prompt for users - required format ``string`` or ``unicode``
* ``CONTENT_EXTENSIONS`` - A list of the *namespaces* used to add additional content types, these are used when discovering the available extensions for about pages - required format a ``list`` of ``strings``


``ARISTOTLE_DOWNLOADS``
-----------------------
This is a **list of tuples** that define the different download options that will
be made available to users::

    #(fileType,menu,font-awesome-icon,module-(unused))


Sample settings
---------------

Below is the ``ARISTOTLE_SETTINGS`` and ``ARISTOTLE_DOWNLOADS`` used on the hosted
Aristotle example::

    ARISTOTLE_SETTINGS = {
       # 'The main title for the site.'
        'SITE_NAME': 'Aristotle Metadata Registry',
       # URL for the Site-wide logo
        'SITE_BRAND': '/static/aristotle_mdr/images/aristotle_small.png',
       # 'Intro text use on the home page as a prompt for users.'
        'SITE_INTRO': 'Use Aristotle Metadata to search for metadata...',
       #Extensions that add additional object types for search/display.
        'CONTENT_EXTENSIONS' : [ 'comet' ]
      }

    ARISTOTLE_DOWNLOADS = [
        ('pdf','PDF','fa-file-pdf-o','module'),
        ('xml','XML','fa-file-code-o','aristotle-xml'),
        ]
