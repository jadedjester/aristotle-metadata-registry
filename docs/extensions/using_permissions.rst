Using Aristotle permissions in custom code
==========================================

One of the key features in Aristotle is specific access control to items based on a
rich matrix of user groups. To make creating extension easier these are exposed through
the code in a number of easy to use ways.

Permissions in ``perms.py``
---------------------------

.. automodule:: aristotle_mdr.perms
   :members: user_can_change_status, user_can_edit, user_can_view

Permissions-based ``ConceptManager``
------------------------------------

All correctly derived ``concept`` items should have their default manager set to
the ``aristotle.models.ConceptManager``. For more information on how this works
see the full documentation on the
:doc:`ConceptManager and ConceptQuerySet <using_concept_manager>`.

.. autoclass:: aristotle_mdr.models.ConceptManager
   :noindex:


Permissions template tags
-------------------------

.. automodule:: aristotle_mdr.templatetags.aristotle_tags
   :members: can_edit, can_view, can_view_iter
   :noindex:

There are more :doc:`template tags available in Aristotle <templatetags>`