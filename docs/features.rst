Features of Aristotle-MDR
=========================

100% Free open-source software
------------------------------
The entire suite of software that Aristotle-MDR is built upon is free open-source software.
The majority of these requirements are managed through the `Python Package Index <https://pypi.python.org/pypi>`_,
the rest are online resources, such as
`jQuery <http://jquery.com/>`_,
`Twitter Bootstrap CSS Framework <http://getbootstrap.com/>`_ and
`Font Awesome <http://fortawesome.github.io/Font-Awesome/>`_ are hosted through online
content delivery networks for improved speed.

Because of the open nature, low-requirements and no-cost of this framework a new registry can be
setup on a Python shared hosting service like `Python Anywhere <www.pythonanywhere.com>`_ in a matter
of minutes - and includes everything you need to get a professional scalable metadata registry up and running.

The only restriction with running Aristotle-MDR is that if you are running a public facing site,
you keep a link to the Aristotle GitHub page in the footer, but even this can can be waived with permission.

Easily extensible
-----------------
One of the core features of the ISO/IEC 11179-3 information model is the ability
to extend the models by subclassing from the included items. Aristotle-MDR captures the
core of the ISO/IEC 11179 as faithfully as possible, but provides a rich API to quickly
and easily add new items for management using the Object-Oriented approach of
`Python <https://www.python.org/>`_ and `Django <https://www.djangoproject.com/>`_.

You can read more about the
:doc:`content type API </extensions/new_content_type>` and
:doc:`template overrides </extensions/templates>` in the
:doc:`extensions documentation </extensions/index>`.

Cross-platform support
----------------------
Built upon `Python <https://www.python.org/>`_ and `Django <https://www.djangoproject.com/>`_,
the Aristotle MetaData Registry can be deployed on a wide range of platform and backend databases
with relative ease, from traditional Linux/Unix/OSX based servers, to
`Windows-based servers <https://docs.djangoproject.com/en/dev/howto/windows/>`_.
The third-party `Django-MSSQL project <http://django-mssql.readthedocs.org/en/latest/>`_
even provides support for the Microsoft MS-SQL database.

On the client, Aristotle MetaData Registry has rich interactive user interface available
on all modern browsers, but includes additional support to allow for management of
content on common legacy browsers as far back as Internet Explorer 8.

Mobile-friendly interface
-------------------------
Every page of Aristotle-MDR has been built upon the `Twitter Bootstrap CSS Framework <http://getbootstrap.com/>`_.
This means that every page has a responsive, mobile first design and flawlessly
scales from the largest desktop to the smallest phone. Along with this, the use of the
`Font Awesome <http://fortawesome.github.io/Font-Awesome/>`_ icon toolkit means menus
and pages have a consistent look and feel.

Real-time enterprise search
---------------------------
Integration of the `Django-Haystack <http://haystacksearch.org/>`_ search API
provides a rich search engine capability, so content can always be found. Content
can be search on not just by text fields, but also by Registration Status, the owner
workgroup and content type, with more advanced search options to come!

Although the default settings for Aristotle use the `Whoosh search engine <https://pypi.python.org/pypi/Whoosh/>`_,
`Haystack provides backend hooks for a number enterprise ready search engines <http://django-haystack.readthedocs.org/en/latest/backend_support.html>`_.

The default settings for Aristotle-MDR include a real-time search index manager
that tracks changes as they are made, and updates visibilty and indexes immediately.

With appropriate tweaking the Haystack engine can scale from the smallest research facility
to the largest government agency.

Secure, thoroughly tested permissions
-------------------------------------
Using a set of thoroughly tested custom permissions, content created within the
Aristotle registry can be show or hidden from the public and registered users
based on the well documented status workflow in part 6 of the ISO/IEC 11179 standard.

Strict version control of the code on `GitHub <https://github.com/LegoStormtroopr/aristotle-metadata-registry/>`_,
continuous testing of the code using `Travis-CI <https://travis-ci.org/LegoStormtroopr/aristotle-metadata-registry>`_
and code coverage analysis using `Coveralls.io <https://coveralls.io/r/LegoStormtroopr/aristotle-metadata-registry>`_
ensures that access permissions are clearly defined, and as changes are made
if issues with permissions they can be idenitified and rectified immediately.

Easy content creation
---------------------
The `Django inplace edit <https://pypi.python.org/pypi/django-inplaceedit>`_ module gives
users the ability to edit content directly on the site and instantly see how content will look.
Using the the `TinyMCE <http://www.tinymce.com/>`_ WYSIWYG (What-You-See-Is-What-You-Get)
editor, users get instant feedback on changes to content.

While not in Aristotle-MDR yet, the Django inplace edit team have also produced
`an inline translation module for django <https://pypi.python.org/pypi/django-inlinetrans>`_ that
allows user to add translations for content without having to navigate away from the content.
Once integrated with Aristotle-MDR this will allow metadata managers to create and manage
multilingual descriptions of data.