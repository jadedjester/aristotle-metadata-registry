Including extra content on pages
================================

Often when adding new content types there will be references to pre-existing items
which may need to be shown on an existing page. While its possible to completely override
a template it can be easier to simply declare any "extra content" ina special template
that Aristotle will then include when rendering the main template. This can be very advantageous when an extension is designed to be included on a
site alongside other extensions.

To do this, all that needs to be done is to include a directory path ``extra_content``
under the template path for your extension. If an entry for the extension has been included
in the Aristotle settings, the main will then look in this directory for templates
with the same name as the currently rendered content type.

For example, the comet extension defines an ``Indicator`` content type that has multiple
references to ``DataElement`` items. Rather than redefine the ``aristotle/concept/dataElement.html``
template, it defines an ``extra_content`` template.

Templates for comet content types are included under ``templates/comet/``. Under this
directory there is a further path ``extra_content``, so by creating a file
named ``dataElement.html`` we can create a template for including extra relationship details.

This will then be rendered in the "Relationships" section of the page.

The full path for a generic extra content template, would be::

    templates/app_name/extra_content/aristotle_content_type.html