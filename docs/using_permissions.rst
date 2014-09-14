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

The ``concept`` abstract class defines a  In ``aristotle.models``

.. autoclass:: aristotle_mdr.models.ConceptManager

Permissions template tags
-------------------------

.. automodule:: aristotle_mdr.templatetags.aristotle_tags
   :members: can_edit, can_view, can_view_iter
