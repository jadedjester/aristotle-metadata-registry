Aristotle Mission Statement
===========================

The core principle behind the design of the Aristotle MetaData Registry is to build
a framework for building compliant ISO/IEC 11179 Metadata Registries, using 100%
Free Open Source Software, and released to the public as Free Open Source Software.

By designing Aristotle-MDR in an extensible way, the core data model of Aristotle aims
to be as close to the model of ISO/IEC 11179-3, without burdening the code with unnecessary objects.

Aristotle-MDR is designed to provide the framework for a metadata registry, and
is explicitly *not* designed to be a standard web content management system, and a core
assumption in the design of Aristotle is that the management of 'non-metadata' content
is a matter for each party installing Aristotle to tackle.

There are some simple url hooks available in Aristotle for including extra pages using the
django template system, alternatively `Django Packages <https://www.djangopackages.com/>`_ has a
list of a number of `excellent CMS packages for Django <https://www.djangopackages.com/grids/g/cms/>`_.
Any of these should quite easily slot in besides the Aristotle app in a custom site,
without having to alter the code or compromise the core principles of Aristotle.