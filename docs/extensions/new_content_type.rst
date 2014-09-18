Making new item types
=====================

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
a ``name`` and ``description``, but also can immediately be associated with a workgroup, can be
registered and progressed within the registry and has all of the correct permissions
associated with all of these actions.

Likewise, creating relationships to pre-existing items only requires the correct
application of `Django relationships <https://docs.djangoproject.com/en/dev/topics/db/examples/>`_
such as like ``ForeignKey`` or ``ManyToManyField``, like so::

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
on DataElements, so that ``myDataElement.question`` would return of all Questions
that are collect information for that Data Element.

Caveats: ``concept`` versus ``_concept``
----------------------------------------

There is a need for some objects to link to any arbitrary concept, for example the
``aristotle.models.Package`` object and the favoruites field of `aristotle.models.AristotleProfile`.
Because of this there is a distinction between a ``concept`` and a ``_concept``.

Abstract base classes in Django allow for the easy creation of items that share
similar properties, without introducing additional fields into the database. They also
allow for self-referential ForeignKeys that are restricted to the inherited type, rather
than to the base type.

.. autoclass:: aristotle_mdr.models._concept
.. autoclass:: aristotle_mdr.models.concept

The correct way to include both of these models is shown below::

    class AReallyComplexExampleItem(concept):
        relatedTo = models.ManyToManyField(_concept)

Retrieving the "true item" when you are returned a ``_concept``.
----------------------------------------------------------------

Because ``_concept`` is not a true abstract class, queries on this table or a Django
``QuerySet`` that reference a ``_concept`` won't return the "actual" object but will
return an object of type ``_concept`` instead. There is a ``item`` property on both the
``_concept`` and ``concept`` classes that will return the properly subclassed item
using the ``get_subclass`` method from ``django-model-utils``.

.. autoattribute:: aristotle_mdr.models._concept.item
.. autoattribute:: aristotle_mdr.models.concept.item

On the inherited ``concept`` class this just returns a reference to the original item - ``self``.
So once the true item is retrieved, this property can be called infinitely without a performance hit.

For example, in code or in a template it is always safe to call an item like so::

    question.item
    question.item.item
    question.item.item.item

When in doubt about what object you are dealing with, calling ``item`` will ensure the
expected item, and not the ``_concept`` parent, is used.
In the very worst case a single additional query is made and the right item is used, in
the best case an very cheap Python property is called and the item is returned straight back.

Creating admin pages for new items types
----------------------------------------

The creation and registration of Admin page is done in the ``admin.py`` file of a Django app.

Because of the intricate permissions around content with the Aristotle Registry,
its recommended that admin pages for new items extend from the existing
``aristotle.admin.ConceptAdmin`` class. This helps to ensure that there is a
consistent ordering of fields, and information is exposed only to the correct
users.

The most important property of the ``ConceptAdmin`` class is the ``fieldsets`` property
that defines the inclusion and ordering of fields within the admin site. The easiest
way to extend this is to add extra options to the end of the ``fieldsets`` like so::

    from aristotle_mdr import admin as aristotle_admin

    ...

    class QuestionAdmin(aristotle_admin.ConceptAdmin):
        fieldsets = aristotle_admin.ConceptAdmin.fieldsets + [
                ('Question Details',
                    {'fields': ['questionText','responseLength']}),
                ('Relations',
                    {'fields': ['collectedDataElement']}),
        ]

**It is important to always import** ``aristotle.admin`` **with an alias as shown above**,
otherwise there are circular dependancies across various apps when importing.
This will prevent the app and the whole site from being used.

`For more information on configuring an admin site for Django models, consult the
Django documentation <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
as well as `the documentation for Grappelli admin extensions <https://django-grappelli.readthedocs.org/>`_.

Making new item types searchable
--------------------------------

The creation and registration of haystack search indexes is done in the ``search_indexes.py`` file of a Django app.

On an Aristotle-MDRpowered site, it is possible to restrcit search results across a number of
criteria including the registration status of an item, its workgroup or Registration
Authority or the item type.

In ``aristotle.search_indexes`` there is the convenience class ``conceptIndex`` that
make registering a new item quite easy, and allows new items to be searched across
these criteria with a minimum of code. Inheriting from this class takes care of nearly
all simple cases when searching for new items, like so::

    from haystack import indexes
    from aristotle_mdr.search_indexes import conceptIndex

    class QuestionIndex(conceptIndex, indexes.Indexable):
        def get_model(self):
            return models.Question

**It is important to import the required models from  ``aristotle.search_indexes``
directly, otherwise there are circular dependancies in Haystack when importing.
This will prevent the app and the whole site from being used.

The only additional work required is to create a search index template in the
``templates`` directory of your app with a path similar to this::

    template/search/indexes/your_app_name/question_text.txt

This ensures that when Haystack is indexing the site, some content is available
so that items can be queried and weighted accordingly. These templates are passed an ``object``
variable that is the particualr object being indexed.

Sample content for an index for our question would look like this::

    {% include "search/indexes/aristotle_mdr/managedobject_text.txt" %}
    {{ object.questionText }}

Here we include the ``managedobject_text.txt`` which adds generic content for all
concepts into the indexed text, as well as including the ``questionText`` in the index.

If we wanted to include the content from the related Data Element to add more search
terms and weighting we could include this as well, using one of the included indexes
in Aristotle, like so::

    {% include "search/indexes/aristotle_mdr/managedobject_text.txt" %}
    {{ object.questionText }}
    {% include "search/indexes/aristotle_mdr/dataelement_text.txt" with object=object.collectedDataElement only %}

`For more information on creating search templates and configuring search options consult the
Haystack documentation <http://django-haystack.readthedocs.org/>`_.

Caveats around extending existing item types
--------------------------------------------

This tutorial has covered how to create new items when inheriting from the base
``concept`` type. However, Python and Django allow for extension from any object.
So if you wished to extend and improve on 11179 item it would be perfectly possible
to do so by inheriting from the appropriate class, rather than the abstract ``concept``.
For example, if you wished to extend a Data Element to create a internationalised
DatElement that was only applicable in specific countries, this could be done like so::

    class Country(model.Models):
        name = models.TextField
        ... # Other attributes could also be applied.

    class CountrySpecificDataElement(aristotle.models.DataElement):
        countries = models.ManyToManyField(Country)

Aristotle does not prevent you from doing so, however there are a few issues that
can arise from doing so.

* All objects subclassed from a concrete model, will also exist in the database as
  an item that belongs to the parent model.

  So a ``CountrySpecificDataElement`` would also be a ``DataElement``, so a query like this::

     aristotle.models.DataElement.objects.all()

  Would return both ``DataElement`` s and ``CountrySpecificDataElement`` s, likewise
  if a ``CountrySpecificDataElement`` is created with the id ``543210``, if a user
  browsed to::

     example.com/your_app_path/countryspecificdataelement/543210

  They would go to the correct page for a ``CountrySpecificDataElement``, however
  if they browsed to::

     example.com/dataelement/543210

  They would be returned a page that showed item ``543210`` as a ``DataElement``.
  Depending on the domain and objects, this may be desired behaviour.

* Following from the above, restricted searchs for the parent item will return
  results from the subclassed ite. In short all searches restricted to a ``DataElement``
  would also return results for ``CountrySpecificDataElement``, and they will
  be displayed in the list as ``DataElement`` *not* as ``CountrySpecificDataElement``.

* Items that inherit from non-abstract classes do not inherit the Django object Mangers,
  this is one of the reasons for the decision to make ``concept`` an abstact class.
  As such, its adviced that any items that inherit from concrete classes refine the
  default object manager like so::

    class CountrySpecificDataElement(aristotle.models.DataElement):
        countries = models.ManyToManyField(Country)
        objects = aristotle_mdr.models.ConceptManager()

Creating ``unmanagedContent`` types
-----------------------------------

Not all content needs to undergo a standardisation process, and in fact some content
should only be accessible to administrators. In Aristotle this is termed an "unmanagedObject".
Content types that are unmanaged do not belong to workgroups, and can only be edited by
users with the Django "super user" privileges.

It is perfectly safe to extend from the ``unmanagedObject`` types, however because these
are closer to pure Django objects there are much fewer convenience method set up to
handle them. By default, ``unmanagedContent`` is always visible.

Because of their visibility and strict privileges, they are generally suited to relatively
static items that may vary between individual sites and add context to other items. Inheriting
from this class can be done like so::

    class Country(aristotle.models.unmanagedObject):
        # Inherits name and description.
        isoCode = models.CharField(maxLength=3)

For example, in Aristotle "Unit of Measure" is an ``unmanagedObject`` type, that is used
to give extra context to Value Domains.


A complete example of an Aristotle Extension
--------------------------------------------
The first package of content extension for Aristotle that helped clarify a lot
of the issues around inheritance was the
`Comet Indicator Registry <https://github.com/LegoStormtroopr/comet-indicator-registry>`_.
This adds 6 new content types along with admin pages, search indexes and templates and includes an override for the
Aristotle ``DataElement`` template - which was all achieved with less than 600 lines of code.