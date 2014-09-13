Using Aristotle permissions in custom code
==========================================

Permissions in ``perms.py``
--------------------------

* user_can_view
* user_can_change_status
* user_can_edit

Permissions template tags
-------------------------

* ``can_view_iter`` - For example::
    {% for item in myItems|can_view_iter:user %}
      {{ item }}
    {% endfor %}

* ``can_view_item`` - For example::
    {% if request.user|can_view_item:myItem %}
      {{ item }}
    {% endif %}

* ``can_edit_item`` - For example::
    {% if request.user|can_edit_item:myItem %}
      {{ item }}
    {% endif %}

Permissions-based ``ConceptManager``
------------------------------------

In ``aristotle.models``