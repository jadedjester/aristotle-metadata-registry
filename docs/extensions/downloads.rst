Adding new download formats
===========================

While the Aristotle-MDR framework includes PDF download capability, it may be desired to download
metadata stored with a registry in a variety of download formats. Rather than include
these within the Aristotle-MDR core codebase, additional downloads can be included via the
download API.

Creating a Django compatible download module
--------------------------------------------

Required files:

* ``__init__.py``
* ``models.py``
* ``download.py``

Writing a ``downloader.download`` method
----------------------------------------

Like this::

    def download(request,downloadType,item):



How the ``download`` view works
-------------------------------

.. automodule:: aristotle_mdr.views
   :members: download
