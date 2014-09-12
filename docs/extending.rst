Extending Aristotle-MDR
=======================



Making new item types
---------------------

Most of the overhead for creating new item types in Aristotle is taken care of by
inheritance within Python language and the Django web framework.

For example, creating a new item within the registry requires as little code as::

    class Question(concept):
        questionText = models.TextField()
        responseLength = models.PositiveIntegerField()

This code creates a new "Question" object in the registry that can be progressed
like any standard item in Aristotle. Once the the appropriate admin pages are
set up, this would be able to be indistinguishable from a Aristotle-MDR item.

Once synced in with the database, this immediately creates a new item type that not only has
a `name` and `description`, but also can immediately be associated with a workgroup, can be
registered and progressed within the registry and has all of the correct permissions
associated with all of these actions.

Likewise, creating relationships to pre-existing items only requires the correct
application of `Django relationships <https://docs.djangoproject.com/en/dev/topics/db/examples/>`_
such as `ForeignKey`s or `ManyToManyField`s, like so::

    import aristotle_mdr

    ...

    class Question(concept):
        questionText = models.TextField()
        responseLength = models.PositiveIntegerField()
        collectedDataElement = models.ForeignKey(
                aristotle_mdr.models.DataElement,
                related_name="questions",
                null=True,blank=True)

This code, extends our Question model from the previous example and adds an optional
link to the 11179 Data Element model managed by Aristotle and includes a new property
on DataElements, so that `myDataElement.questions` would return of all `Question`s
that are collect information for that Data Element.

Caveats: `concept` versus `_concept`
++++++++++++++++++++++++++++++++++++

There is a need for some objects to link to any arbitrary concept, for example the
`aristotle.models.Package` object and the favoruites field of `aristotle.models.AristotleProfile`.
Because of this there is a distinction between a `concept` and a `_concept`.

Abstract base classes in Django allow for the easy creation of items that share
similar properties, without introducing additional fields into the database. They also
allow for self-referential ForeignKeys that are restricted to the inherited type, rather
than to the base type.

* `_concept` is the base concrete class that `Status` items attach to, and to which
collection objects refer to. It is not marked abstract in the Django Meta class, and
**must not be inherited from**. It has relatively few fields and is a convenience
class to link with.
* `concept` is an abstract class that all items that should behave like 11179 Concept
**must** inherit from. This includes the definitions for many long and optional text
fields and the self-referential `superseded_by` field. It is not possible to include this
model in a `ForeignKey` or `ManyToManyField`.

The correct way to include both of these models is shown below::

    class ComplexExampleItem(concept):
        relatedTo = models.ManyToManyField(_concept)


Creating admin pages for new items types
----------------------------------------

Because of the intricate permissions around content with the Aristotle Registry,
its recommended that admin pages for new items extend from the existing
`aristotle.admin.ConceptAdmin` class. This helps to ensure that there is a
consistent ordering of fields, and information is exposed only to the correct
users.

The most important property of the `ConceptAdmin` class is the `fieldsets` property
that defines the inclusion and ordering of fields within the admin site. The easiest
way to extend this is to add extra options to the end of the `fieldsets` like so::

    class QuestionAdmin(aristotle_admin.ConceptAdmin):
        fieldsets = aristotle_admin.ConceptAdmin.fieldsets + [
                ('Question Details',
                    {'fields': ['questionText','responseLength']}),
                ('Relation',
                    {'fields': ['collectedDataElement']}),
        ]

`For more information on configuring an admin site for Django models, consult the
Django documentation <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
as well as `the documentation for Grappelli admin extensions <https://django-grappelli.readthedocs.org/>`_.

Adding search for new item types
--------------------------------

Caveats around extending existing item types
++++++++++++++++++++++++++++++++++++++++++++
