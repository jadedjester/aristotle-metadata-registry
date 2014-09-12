=====
Aristotle MetaData Registry (Aristotle-MDR)
=====

Aristotle-MDR is an open-source metadata registry as laid out by the requirements
of the ISO/IEC 11179:2013 specification.

Aristotle-MDR represents a new way to manage and federate content built on and extending
the principles of leading metadata registry. The code of Aristotle is completely open-source,
building on the Django web framework and the mature model of the 11179 standard,
agencies can easily run their own metadata registries while also having the ability
to extend the information model and tap into the permissions and roles of ISO 11179.

By allowing organisations to run their own independant registries the are able to
expose authoritative metadata and the governance processes behind its creation,
and building upon known and open systems agencies, can build upon a stable platform
or the sharing of 11179 metadata items.

Quick start
-----------

1. Add "aristotle_mdr" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'haystack',
        'aristotle_mdr',
        'grappelli',
        ...
    )

   To ensure that search indexing works properly `haystack` **must** be installed before `aristotle_mdr`.
   If you want to take advantage of Aristotle's access-key shortcut improvements for the admin interface,
   make sure it is installed *before* `grappelli`.

   Some Aristotle extensions (such as the Comet Indicator Registry Plug-ins) override aristotle templates
   to add additional content to registry pages. For these overrides to be active extensions must be
   installed before aristotle like this::

    INSTALLED_APPS = (
        ...
        'comet',
        'aristotle_mdr',
        '...',
    )


2. Include the Aristotle-MDR URLconf in your project urls.py. Because Aristotle will
   form the majority of the interactions with the site, and the Aristotle includes a
   number of URLconfs for supporting apps its recommended to included it at the
   server root, like this::

    url(r'^/', include('aristotle_mdr.urls')),

3. Run `python manage.py migrate` to create the Aristotle Database.

4. Start the development server and visit http://127.0.0.1:8000/
   to see the home page.

For a complete example of how to successfully include Aristotle, see the `example_app` directory.
