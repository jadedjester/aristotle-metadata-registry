Adding new static pages into Aristotle
======================================

While Aristotle provides a strong framework for setting up a metadata registry,
there some static pages which are important for a site, but unlikely to be changed,
such as the home page, CSS and about pages.

These exist in aristotle as template pages, and like all Django tempaltes are easy to
override with more custom, site-specific content. The first step is to ensure the
settings for the site include a Django ``TEMPLATE_DIR`` directive, like that below::

    TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

Setting a separate template directory when using Aristotle ensure that templates
can be easily overriden, without requiring a separate django app or editing of
the main Aristole codebase.

When attempting to resolve templates, one of the first locations checked will be the
directory stated in ``TEMPLATE_DIRS``. Examining the
`Aristotle-MDR <https://github.com/LegoStormtroopr/aristotle-metadata-registry/>`_
should give an understanding of how the templates are laid out if changes are necessary.

Recommended pages
-----------------

A number of site specific pages are expected to exist, and Aristotle includes some
very basic boilerplate for these, but it is strongly recommended these are overridden.

Under the ``site/`` template path are the following pages::

* ``about.html`` - This link is used for explaining what this particular site is
  trying to achieve. When browsing the site it is avaiable at ``http://mysite.org/about/``.
* ``accessibility.html`` - A page explaining the accessibility requirements for this site.
  The boilerplate is quite extensive and may be used as is, but if overriding this template it is
  recommended the list of quick keys is kept. When browsing the site it is avaiable at ``http://mysite.org/accessibility/``.
* ``copyright.html`` - A page indicating the copyright status. The boilerplate indicates that all
  content is the explicit propery of the site, but it is strongly recommended that this be changed accordingly.
  When browsing the site it is avaiable at ``http://mysite.org/copyright/``.
* ``disclaimer.html`` - A page indicating the fitness for purpose of the content of the site. Due to the legal nature, it
  is strongly recommended this is overridden.
  When browsing the site it is avaiable at ``http://mysite.org/disclaimer/``.
* ``contact.html`` -  Contact details for site administrators.
  When browsing the site it is avaiable at ``http://mysite.org/contact/``.
* ``privacy.html`` - A page giving the privacy statement of the site. Due to the legal nature, it
  is strongly recommended this is overridden. When browsing the site it is avaiable at ``http://mysite.org/privacy/``.
