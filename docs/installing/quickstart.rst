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
