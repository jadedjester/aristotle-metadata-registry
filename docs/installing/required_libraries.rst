Django
------

> `Django is a high-level Python Web framework that encourages rapid development and
> clean, pragmatic design. <https://www.djangoproject.com/>`_

    1. Python Packager PIP: eg. `sudo apt-get install python-pip`
        This makes installing Python packages much easier. Installation steps assume this is done, but any method can be used to install the required libraries.


1. Install admin tools
    1. Python Packager PIP: eg. `sudo apt-get install python-pip`
        This makes installing Python packages much easier. Installation steps assume this is done, but any method can be used to install the required libraries.
    2. Apache web server: eg. `sudo apt-get install apache2`

2. Install required libraries
    1. [Django](https://www.djangoproject.com): `pip install django>=1.6.0`
    2. [South](http://south.aeracode.org):  `pip install django-south>=0.8.4`

        Used to manage database migrations.

    3. [Haystack](http://haystacksearch.org): `pip install django-haystack>=2.0.0`

        Flexible search engine manager for Django, that allows user choice of a range of search providers. This requires the user to also install a preferred search engine and configure Haystack.

        If you get the `AttributeError at /search/` `'Options' object has no attribute '_fields' ` its because you are using the Haystack simple backend (i.e. you are in development). In that case, you might want to [update to a new version of Haystack](http://stackoverflow.com/questions/21127072/django-haystack-without-attribute-fields)

    4. [In-place edit](https://pypi.python.org/pypi/django-inplaceedit) `pip install django-inplaceedit`

        What the name says on the box. An inplace editor for many fields in django.

    5. [In-place edit Extra fields](https://pypi.python.org/pypi/django-inplaceedit-extra-fields) `pip install django-inplaceedit-extra-fields`

        Adds a few extra fields, good for the auto-lookup via ForeignKey and Many-to-many fields.

    6. [Django Tinymce](https://github.com/aljosa/django-tinymce) `pip install django-tinymce`

        Adds richtext editing options.

    7. [Grappelli](http://grappelliproject.com/) `pip install django-grappelli`

        Prettier admin interface.

    8. [Django-model-utils](https://django-model-utils.readthedocs.org/en/latest/) `pip install django-model-utils`

        Adds some nice syntax for additional models, also allows for determining inheritance of objects.

    9. [django-reversion-compare](https://github.com/jedie/django-reversion-compare) `pip install django-reversion-compare`
        Perhaps install by this: `pip install -e git+git://github.com/jedie/django-reversion-compare#egg=django-reversion-compare` as there is an import bug.
        Includes django-reversion, installing these gives version control, rollback and diff display.

    10. [Diff patch](http:///) `pip install diff-match-patch`

    11. [World Timezone Definitions for Python](http://pytz.sourceforge.net/) `pip install pytz`

    12. [Django Constance](https://pypi.python.org/pypi/django-constance) `pip install django-constance`

         Provides live settings so users can use the front end to change site wide config details such as the site name, styles, etc...

         Constance has some issues with Django 1.6 that are yet to be resolved, if there are issues due to "Meta_fields" not being found install from git: `pip install -e git+git://github.com/comoga/django-constance#egg=django-constance`

    13. [Django picklefield](https://pypi.python.org/pypi/django-picklefield) `pip install django-picklefield`

         Required for Constance to store Python fields to the database.

    14. [xhtml2pdf](https://pypi.python.org/pypi/xhtml2pdf) `pip install xhtml2pdf`

        Used for generating PDFs for downloads. As this compiles C-libraries, this may require the `python-dev` package on Ubuntu which can be installed with `sudo apt-get install python-dev`.

    15. [django-bootstrap3](https://github.com/dyve/django-bootstrap3) `pip install django-bootstrap3`

    16. [django-bootstrap3-datetimepicker](https://github.com/dyve/django-bootstrap3-datetimepicker) `pip install django-bootstrap3-datetimepicker`
    <!--5. [](http://) `pip install `-->
