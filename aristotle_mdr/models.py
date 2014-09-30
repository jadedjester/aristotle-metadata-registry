from __future__ import unicode_literals

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save,m2m_changed
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager, InheritanceQuerySet
from model_utils.models import TimeStampedModel
from model_utils import Choices, FieldTracker
from notifications import notify
from django.dispatch import receiver

import datetime
from tinymce.models import HTMLField
from aristotle_mdr import perms

# 11179 States
# When used these MUST be used as IntegerFields to allow status comparison
STATES = Choices (
           (0,'notprogressed',_('Not Progressed')),
           (1,'incomplete',_('Incomplete')),
           (2,'candidate',_('Candidate')),
           (3,'recorded',_('Recorded')),
           (4,'qualified',_('Qualified')),
           (5,'standard',_('Standard')),
           (6,'preferred',_('Preferred Standard')),
           (7,'superseded',_('Superseded')),
           (8,'retired',_('Retired')),
         )

class baseAristotleObject(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = HTMLField()
    objects = InheritanceManager()

    class Meta:
        verbose_name = "item" # So the url_name works for items we can't determine
        #Can't be abstract as we need unique app wide IDs.
        abstract = True

    def was_modified_recently(self):
        return self.modified >= timezone.now() - datetime.timedelta(days=1)
    was_modified_recently.admin_order_field = 'modified'
    was_modified_recently.boolean = True
    was_modified_recently.short_description = 'Modified recently?'


    def __unicode__(self):
        return "{name}".format(name = self.name)

    # defined so we can access it during templates
    def get_verbose_name(self):
        return self._meta.verbose_name.title()
    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural.title()
    def url_name(self):
        s = "".join(self._meta.verbose_name.title().split())
        s = s[0].lower() + s[1:]
        return s
    def template_name(self):
        s = "".join(self._meta.verbose_name.title().split())
        s = s[0].lower() + s[1:]
        return s
    # These are all overridden elsewhere, but we use them in permissions instead of inspecting objects to find type.
    @property
    def is_managed(self):
        return False
    @property
    def is_workgroup(self):
        return False

class unmanagedObject(baseAristotleObject):
    class Meta:
        abstract = True
    @property
    def item(self):
        return self

#Pseudo-abstract: Can't actually abstract as 'tracker' isn't pulled across into the children
class registryGroup(unmanagedObject):
    tracker=FieldTracker()

    def save(self, **kwargs):
        for role,permissions in self.__class__.roles.items():
            if self.pk is None:
                # Is this a new item? If so create permissions
                group,created = Group.objects.get_or_create(name="{name} {role}".format(name=self.name,role=role))
                content_type = ContentType.objects.get_for_model(_concept)
                for name,code in permissions:
                    perm,created = Permission.objects.get_or_create(codename=code.format(name=self.name),
                                                            name=name.format(name=self.name),
                                                            content_type=content_type)
                    group.permissions.add(perm)
            elif self.tracker.has_changed('name'):
                # If we have changed the name, update the permissions
                prev = self.tracker.previous('name')
                g = Group.objects.get(name="{name} {role}".format(name=prev, role=role))
                g.name = "{name} {role}".format(name=self.name, role=role)
                g.save()
                for name,code in permissions:
                    p = Permission.objects.get(codename=code.format(name=prev))
                    p.codename = code.format(name=self.name)
                    p.save()
        super(registryGroup, self).save(**kwargs)

    def giveRoleToUser(self,role,user):
        if role in self.__class__.roles.keys():
            g = Group.objects.get(name="{name} {role}".format(name=self.name, role=role))
            g.user_set.add(user)

    def removeRoleFromUser(self,role,user):
        if role in self.__class__.roles.keys():
            g = Group.objects.get(name="{name} {role}".format(name=self.name, role=role))
            g.user_set.remove(user)

"""
A registration authority is a proxy group that describes a governance process for "standardising" metadata.
"""
class RegistrationAuthority(registryGroup):
    template = "aristotle_mdr/registrationAuthority.html"
    locked_state = models.IntegerField(choices=STATES, default=STATES.candidate)
    public_state = models.IntegerField(choices=STATES, default=STATES.recorded)

    # The below text fields allow for brief descriptions of the context of each
    # state for a particular Registration Authority
    # For example:
    # For a particular Registration Authority standard may mean"
    #   "Approved by a simple majority of the standing council of metadata standardisation"
    # While "Preferred Standard" may mean:
    #   "Approved by a two-thirds majority of the standing council of metadata standardisation"

    notprogressed = models.TextField(blank=True)
    incomplete = models.TextField(blank=True)
    candidate = models.TextField(blank=True)
    recorded = models.TextField(blank=True)
    qualified = models.TextField(blank=True)
    standard = models.TextField(blank=True)
    preferred = models.TextField(blank=True)
    superseded = models.TextField(blank=True)
    retired = models.TextField(blank=True)

    roles = { 'Registrar':[
                    ('Extract dictionary for {name}','extract_dict_in_{name}'),
                    ('Manage dictionary for {name}','manage_dict_in_{name}'),
                    ('Promote content for {name}','promote_in_{name}'),
                    ('View registered content for {name}','view_registered_in_{name}'),
                    ],
            }
    class Meta:
        verbose_name_plural = _("Registration Authorities")

    @property
    def unlocked_states(self):
        return range(STATES.notprogressed,self.locked_state)
    @property
    def locked_states(self):
        return range(self.locked_state,self.public_state)
    @property
    def public_states(self):
        return range(self.public_state,STATES.retired+1)

    def statusDescriptions(self):
        descriptions =[
            self.notprogressed,
            self.incomplete,
            self.candidate,
            self.recorded,
            self.qualified,
            self.standard,
            self.preferred,
            self.superseded,
            self.retired
        ]

        unlocked = [(STATES[i],descriptions[i]) for i in self.unlocked_states]
        locked = [(STATES[i],descriptions[i]) for i in self.locked_states]
        public = [(STATES[i],descriptions[i]) for i in self.public_states]

        return (('unlocked',unlocked),('locked',locked),('public',public))

    def register(self,item,state,user,regDate=timezone.now(),cascade=False):
        reg,created = Status.objects.get_or_create(
                concept=item,
                registrationAuthority=self,
                defaults ={
                    "registrationDate" : regDate,
                    "state" : state
                    }
                )
        if not created:
            reg.state = state
            reg.registrationDate = regDate
            reg.save()
        if cascade:
            for i in item.registryCascadeItems:
                if i is not None and perms.user_can_change_status(user,i):
                   self.register(i,state,user,regDate,cascade)
        return reg

    def giveRoleToUser(self,role,user):
        super(RegistrationAuthority, self).giveRoleToUser(role,user)
        user.profile.registrationAuthorities.add(self)


"""
A workgroup is a collection of associated users given control to work on a specific piece of work. usually this work will be a specific collection or subset of objects, such as data elements or indicators, for a specific topic.

Workgroup owners may choose to 'archive' a workgroup. All content remains visible,
but the workgroup is hidden in lists.
"""
class Workgroup(registryGroup):
    template = "aristotle_mdr/workgroup.html"
    archived = models.BooleanField(default=False)
    registrationAuthorities = models.ManyToManyField(
            RegistrationAuthority, blank=True, null=True,
            related_name="workgroups",
            )

    roles = { 'Viewer':[
                    ('View content in workgroup {name}','view_in_{name}'),
                    ],
              'Editor':[
                    ('View content in workgroup {name}','view_in_{name}'),
                    ('Create content in workgroup {name}','create_in_{name}'),
                    ('Edit Unlocked content in workgroup {name}','edit_unlocked_in_{name}'),
                    ('Register content in workgroup {name}','register_in_{name}'),
                    ],
              'Super-Editor':[
                    ('View content in workgroup {name}','view_in_{name}'),
                    ('Create content in workgroup {name}','create_in_{name}'),
                    ('Edit Unlocked content in workgroup {name}','edit_unlocked_in_{name}'),
                    ('Edit LOCKED content in workgroup {name}','edit_locked_in_{name}'),
                    ('Register content in workgroup {name}','register_in_{name}'),
                    ],
              'Manager':[
                    ('View content in workgroup {name}','view_in_{name}'),
                    ('Create content in workgroup {name}','create_in_{name}'),
                    ('Administrate workgroup {name}','admin_in_{name}'),
                    ]
            }

    def giveRoleToUser(self,role,user):
        super(Workgroup, self).giveRoleToUser(role,user)
        if self not in user.profile.workgroups.all():
            user.profile.workgroups.add(self)

    def addUser(self,user):
        if self not in user.profile.workgroups.all():
            user.profile.workgroups.add(self)
        self.giveRoleToUser("Viewer",user)

    def removeUser(self,user):
        if self in user.profile.workgroups.all():
            user.profile.workgroups.remove(self)
        for role in Workgroup.roles.keys():
            self.removeRoleFromUser(role,user)

    @property
    def classedItems(self):
        # Convenience class as we can't call functions in templates
        return self.items.select_subclasses()

    @property
    def is_workgroup(self):
        return True
    @property
    def managers(self):
        return Group.objects.get(name="{name} {role}".format(name=self.name, role='Manager')).user_set.all()
    @property
    def super_editors(self):
        return Group.objects.get(name="{name} {role}".format(name=self.name, role='Super-Editor')).user_set.all()
    @property
    def editors(self):
        return Group.objects.get(name="{name} {role}".format(name=self.name, role='Editor')).user_set.all()
    @property
    def viewers(self):
        return Group.objects.get(name="{name} {role}".format(name=self.name, role='Viewer')).user_set.all()

class discussionAbstract(TimeStampedModel):
    body = models.TextField()
    author = models.ForeignKey(User)
    class Meta:
        ordering = ['-modified']
        abstract = True
    @property
    def edited(self):
        return self.created != self.modifed

class DiscussionPost(discussionAbstract):
    workgroup = models.ForeignKey(Workgroup)
    title = models.CharField(max_length=256)
    relatedItems = models.ManyToManyField('_concept',blank=True,
                    related_name='relatedDiscussions',
                    )
    closed = models.BooleanField(default=False)
    @property
    def active(self):
        return not self.closed

class DiscussionComment(discussionAbstract):
    post = models.ForeignKey(DiscussionPost, related_name='comments')

#class ReferenceDocument(models.Model):
#    url = models.URLField()
#    description = models.TextField()
#    object = models.ForeignKey(managedObject)

class ConceptQuerySet(InheritanceQuerySet):
    def editable(self,user):
        """
        Returns a list of items from the queryset the user can edit.

        This isn't actually a query set, as it returns a list of items instead of an actual
        ``Queryset`` object. As such this is unchainable after this is called, and **must**
        be the last call in a queryset chain. For example, this will work::

            ObjectClass.objects.filter(name__contains="Person").editable()

        But this will break::

            ObjectClass.objects.editable().filter(name__contains="Person")

        However, because querysets and lists are both iterable, in most cases this is safe to use.
        If you need a queryset of `editable` items, use ``editable_slow``.
        """
        return [i for i in self.all() if perms.user_can_edit(user,i)]
    def visible(self,user):
        """
        Returns a list of items from the queryset the user can view.

        This isn't actually a query set, as it returns a list of items instead of an actual
        ``Queryset`` object. As such this is unchainable after this is called, and **must**
        be the last call in a queryset chain. For example, this will work::

            ObjectClass.objects.filter(name__contains="Person").visible()

        But this will break::

            ObjectClass.objects.visible().filter(name__contains="Person")

        However, because querysets and lists are both iterable, in most cases this is safe to use.
        If you need a queryset of `visible` items, use ``visible_slow``.
        """
        return [i for i in self.all() if perms.user_can_view(user,i)]
    def public(self):
        """
        Returns a list of public items from the queryset.

        This isn't actually a query set, as it returns a list of items instead of an actual
        ``Queryset`` object. As such this is unchainable after this is called, and **must**
        be the last call in a queryset chain. For example, this will work::

            ObjectClass.objects.filter(name__contains="Person").public()

        But this will break::

            ObjectClass.objects.public().filter(name__contains="Person")

        However, because querysets and lists are both iterable, in most cases this is safe to use.
        If you need a queryset of `public` items, use ``public_slow``.
        """
        return [i for i in self.all() if i.is_public()]

    # The below return actual querysets, but are much slower
    # They hit the database twice, once to get the item ids and again to get the matching objects
    def editable_slow(self,user):
        """
        This is a slow wrapper around `editable` that queries for items a user can edit
        and then requeries the database for items that match the ids of the initial
        query.

        It is **slow, but chainable**. It is recommended that this the very last query
        after the querset in a chain so it is as small as possible, and is only used
        where a `QuerySet`` is absolutely required.

         For example, both of these will work::

            ObjectClass.objects.filter(name__contains="Person").editable()
            ObjectClass.objects.editable().filter(name__contains="Person")
        """
        return self.filter(id__in=[i.id for i in self.editable(user)])
    def visible_slow(self,user):
        """
        This is a slow wrapper around `visible` that queries for items a user can view
        and then requeries the database for items that match the ids of the initial
        query.

        It is **slow, but chainable**. It is recommended that this the very last query
        after the querset in a chain so it is as small as possible, and is only used
        where a `QuerySet`` is absolutely required.

         For example, both of these will work::

            ObjectClass.objects.filter(name__contains="Person").visible()
            ObjectClass.objects.visible().filter(name__contains="Person")
        """
        return self.filter(id__in=[i.id for i in self.visible(user)])
    def public_slow(self):
        """
        This is a slow wrapper around `public` that queries for items that are public
        and then requeries the database for items that match the ids of the initial
        query.

        It is **very very slow, but chainable**. It is recommended that this the very last query
        after the querset in a chain so it is as small as possible, and is only used
        where a `QuerySet`` is absolutely required.

         For example, both of these will work::

            ObjectClass.objects.filter(name__contains="Person").public()
            ObjectClass.objects.public().filter(name__contains="Person")
        """
        return self.filter(id__in=[i.id for i in self.public()])

class ConceptManager(InheritanceManager):
    """The ``ConceptManager`` is the default object manager for ``concept`` and
    ``_concept`` items, and extends from the django-model-utils ``InheritanceManager``.

    It provides access to the ``ConceptQuerySet`` to allow for easy permissions-based
    filtering of ISO 11179 Concept-based items.
    """
    def get_query_set(self):
        return ConceptQuerySet(self.model)
    def get_queryset(self):
        return ConceptQuerySet(self.model)
    def __getattr__(self, attr, *args):
        # Only let the slow ones through to the queryset
        if attr in ['editable_slow','visible_slow','public_slow']:
            return getattr(self.get_queryset(), attr, *args)
        else:
            return getattr(self.__class__, attr, *args)

class _concept(baseAristotleObject):
    """
    This is the base concrete class that `Status` items attach to, and to which
    collection objects refer to. It is not marked abstract in the Django Meta class, and
    **must not be inherited from**. It has relatively few fields and is a convenience
    class to link with in relationships.
    """
    objects = ConceptManager()
    template = "aristotle_mdr/concepts/managedContent.html"
    readyToReview = models.BooleanField(default=False)
    workgroup = models.ForeignKey(Workgroup,related_name="items")

    class Meta:
        verbose_name = "item" # So the url_name works for items we can't determine
    @property
    def item(self):
        """
        Performs a lookup using ``model_utils.managers.InheritanceManager`` to find the
        subclassed item
        """
        return _concept.objects.get_subclass(pk=self.id)

    def relatedItems(self,user=None):
        return []

    def get_autocomplete_name(self):
        return 'Autocomplete'+"".join(self._meta.verbose_name.title().split())
    """@staticmethod
    def autocomplete_search_fields(self):
        return ("name__icontains",) # Is this right?"""
    def get_absolute_url(self):
        return reverse("aristotle:item",args=[self.id])

    # This returns the items that can be registered along with the this item.
    # Reimplementations of this MUST return lists
    @property
    def registryCascadeItems(self):
        return []
    @property
    def is_managed(self):
        return True
    @property
    def is_registered(self):
        return self.statuses.count() > 0

    @property
    def is_superseded(self):
        return all(STATES.superseded == status.state for status in self.statuses.all()) and self.superseded_by

    @property
    def is_retired(self):
        return all(STATES.retired == status.state for status in self.statuses.all())and self.statuses.count() > 0

    def is_public(self):
        """
            An object is public if any registration authority has advanced it to a public state for THAT RA.
            TODO: Limit this so onlt RAs who are part of the "owning" workgroup are checked
                  This would prevent someone from a different work group who can see it advance it in THEIR RA to public.
        """
        return True in [s.state >= s.registrationAuthority.public_state for s in self.statuses.all()]
    is_public.boolean = True
    is_public.short_description = 'Public'
    def is_locked(self):
        return True in [s.state >= s.registrationAuthority.locked_state for s in self.statuses.all()]
    is_locked.boolean = True
    is_locked.short_description = 'Locked'

class concept(_concept):
    """
    This is an abstract class that all items that should behave like 11179 Concept
    **must be inherited from**. This model includes the definitions for many long and optional text
    fields and the self-referential ``superseded_by`` field. It is not possible to include this
    model in a ``ForeignKey`` or ``ManyToManyField``.
    """
    shortName = models.CharField(max_length=100,blank=True)
    version = models.CharField(max_length=20,blank=True)
    synonyms = models.CharField(max_length=200, blank=True)
    references = HTMLField(blank=True)
    originURI = models.URLField(blank=True) # If imported/migrated, where did this object come from?

    # superseded_by = models.ForeignKey('managedObject', related_name='supersedes',blank=True,null=True)
    # TODO: switch above with below, try and get a generic reference.
    superseded_by = models.ForeignKey('self', related_name='supersedes',blank=True,null=True)

    objects = ConceptManager()

    class Meta:
        abstract = True

    @property
    def item(self):
        """
        Return self, because we already have the correct item.
        """
        return self

    @property
    def getPdfItems(self):
        return {}

class Status(TimeStampedModel):
    concept = models.ForeignKey(_concept,related_name="statuses")
    registrationAuthority = models.ForeignKey(RegistrationAuthority)
    changeDetails = models.CharField(max_length=100)
    state = models.IntegerField(choices=STATES, default=STATES.incomplete)

    inDictionary = models.BooleanField(default=True)
    registrationDate = models.DateField()
    tracker=FieldTracker()

    # TODO: Make it so that an object can only have one status per authority
    class Meta:
        unique_together = ('concept', 'registrationAuthority',)
        verbose_name_plural = "Statuses"

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('concept', 'registrationAuthority',):
            return _('This Object %(obj)s already has a status in Registration Authority "%(ra)s". Please update the exisiting status field instead of creating a new one.')%\
                    {'obj': self.concept,
                      'ra': self.registrationAuthority.name
                    }
        else:
            return super(Status, self).unique_error_message(model_class, unique_check)

    def save(self, *args, **kwargs):
        prev_state=self.tracker.previous('state')
        if prev_state is None:
            prev_state_name = 'Unregistered'
        else:
            prev_state_name=STATES[prev_state]
        obj = super(Status, self).save(*args, **kwargs)
        if prev_state != self.state:
            for p in self.concept.favourited_by.all():
                pass
                #notify.send(p.user, recipient=p.user, verb="changed the status of a favourite item", target=self.concept,
                #description='The state has gone from %s to %s in Registration Authority "%s"'%(prev_state_name,self.state_name,self.registrationAuthority.name)
                #)
        return obj

    @property
    def state_name(self):
        return STATES[self.state]

    def __unicode__(self):
        return "{obj} is {stat} for {ra}".format(
                obj = self.concept.name,
                stat=self.state_name,
                ra=self.registrationAuthority
            )

class ObjectClass(concept):
    template = "aristotle_mdr/concepts/objectClass.html"

    class Meta:
        verbose_name_plural = "Object Classes"

    def relatedItems(self,user=None):
        return [s for s in self.dataelementconcept_set.all() if perms.user_can_view(user,s)]

class Property(concept):
    template = "aristotle_mdr/concepts/property.html"
    class Meta:
        verbose_name_plural = "Properties"

class Measure(unmanagedObject):
    pass
class UnitOfMeasure(unmanagedObject):
    template="aristotle_mdr/unmanaged/unitOfMeasure.html"

    measure = models.ForeignKey(Measure)
    symbol =  models.CharField(max_length=20,blank=True)
class DataType(concept):
    template = "aristotle_mdr/concepts/dataType.html"
    pass

class ConceptualDomain(concept):
    pass

class RepresentationClass(unmanagedObject):
   pass

class ValueDomain(concept):
    template = "aristotle_mdr/concepts/valueDomain.html"
    format = models.CharField(max_length=100)
    maximumLength = models.PositiveIntegerField()
    unitOfMeasure = models.ForeignKey(UnitOfMeasure,blank=True,null=True)
    dataType = models.ForeignKey(DataType)

    conceptualDomain = models.ForeignKey(ConceptualDomain,blank=True,null=True)
    representationClass =  models.ForeignKey(RepresentationClass,blank=True,null=True)

class PermissibleValue(models.Model):
    value = models.CharField(max_length=20)
    meaning = models.CharField(max_length=100)
    valueDomain = models.ForeignKey(ValueDomain,related_name="permissibleValues")
    order = models.PositiveSmallIntegerField("Position")
    def __unicode__(self):
        return "%s: %s - %s"%(self.valueDomain.name,self.value,self.meaning)
    class Meta:
        ordering = ['order']

class SupplementaryValue(models.Model):
    value = models.CharField(max_length=20)
    meaning = models.CharField(max_length=100)
    valueDomain = models.ForeignKey(ValueDomain,related_name="supplementaryValues")
    order = models.PositiveSmallIntegerField("Position")
    def __unicode__(self):
        return "%s: %s - %s"%(self.valueDomain.name,self.value,self.meaning)
    class Meta:
        ordering = ['order']

class DataElementConcept(concept):
    property_ = property #redefine in this context as we need 'property' for the 11179 terminology
    template = "aristotle_mdr/concepts/dataElementConcept.html"
    objectClass = models.ForeignKey(ObjectClass,blank=True,null=True)
    property = models.ForeignKey(Property,blank=True,null=True)
    conceptualDomain = models.ForeignKey(ConceptualDomain,blank=True,null=True)

    @property_
    def registryCascadeItems(self):
        return [self.objectClass,self.property]

# Yes this name looks bad - blame 11179:3:2013 for renaming "administered item" to "concept"
class DataElement(concept):
    template = "aristotle_mdr/concepts/dataElement.html"
    dataElementConcept = models.ForeignKey(DataElementConcept,verbose_name = "Data Element Concept",blank=True,null=True)
    valueDomain = models.ForeignKey(ValueDomain,verbose_name = "Value Domain",blank=True,null=True)

    @property
    def registryCascadeItems(self):
        return [self.dataElementConcept,self.valueDomain]


class DataElementDerivation(concept):
    derives = models.ForeignKey(DataElement,related_name="derived_from")
    inputs = models.ManyToManyField(DataElement,
                related_name="input_to_derivation",
                blank=True,null=True)
    derivation_rule = models.TextField(blank=True)


class Package(concept):
    items = models.ManyToManyField(_concept,related_name="packages",blank=True,null=True)
    template = "aristotle_mdr/concepts/package.html"

    @property
    def classedItems(self):
        return self.items.select_subclasses()

class GlossaryItem(unmanagedObject):
    pass

class GlossaryAdditionalDefinition(models.Model):
    glossaryItem = models.ForeignKey(GlossaryItem,related_name="alternate_definitions")
    registrationAuthority = models.ForeignKey(RegistrationAuthority)
    description = models.TextField()

# Create a 1-1 user profile so we don't need to extend user
# Thanks to http://stackoverflow.com/a/965883/764357
class PossumProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    registrationAuthorities = models.ManyToManyField(
            RegistrationAuthority, blank=True,
            verbose_name="Registration Authorities",
            )
    savedActiveWorkgroup = models.ForeignKey(Workgroup,blank=True,null=True)
    workgroups = models.ManyToManyField(Workgroup,related_name="members",blank=True)
    favourites = models.ManyToManyField(_concept,related_name='favourited_by',blank=True)

    # Override save for inline creation of objects.
    # http://stackoverflow.com/questions/2813189/django-userprofile-with-unique-foreign-key-in-django-admin
    def save(self, *args, **kwargs):
        try:
            existing = PossumProfile.objects.get(user=self.user)
            self.id = existing.id #force update instead of insert
        except PossumProfile.DoesNotExist:
            pass
        models.Model.save(self, *args, **kwargs)

    @property
    def activeWorkgroup(self):
        return self.savedActiveWorkgroup or self.workgroups.first() or self.myWorkgroups.first()

    @property
    def myWorkgroups(self):
        if self.user.is_superuser:
            return Workgroup.objects.all()
        else:
            return self.workgroups.filter(archived=False)

    @property
    def myFavourites(self):
        return self.favourites.select_subclasses()

    @property
    def is_registrar(self):
        return perms.user_is_registrar(self.user)

    @property
    def discussions(self):
        return DiscussionPost.objects.filter(workgroup__in=self.myWorkgroups.all())

    @property
    def registrarAuthorities(self):
        """NOTE: This is a list of Authorities the user is a *registrar* in!."""
        if self.user.is_superuser:
                return RegistrationAuthority.objects.all()
        else:
            return (r for r in self.registrationAuthorities.all()
                if self.user.has_perm('aristotle_mdr.promote_in_{name}'.format(name=r.name)))

    def is_workgroup_manager(self,wg):
        return perms.user_is_workgroup_manager(self.user,wg)

    def isFavourite(self,item_id):
        return self.favourites.filter(pk=item_id).exists()

    def toggleFavourite(self, item):
        if self.isFavourite(item):
            self.favourites.remove(item)
        else:
            self.favourites.add(item)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = PossumProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)

#"""
#A collection is a user specified ad-hoc, sharable collections of content.
#Collection owners can add and remove other owners, editors and viewers
#                  and add or remove content from the collection
#           editors can add or remove content from the collection
#           viewers can see content in the collection
#In all cases, people can only see or add content they have permission to view in the wider registry.
#"""
#class Collection(models.Model):
#    managedObject = models.ForeignKey(trebleObject,related_name='in_collections')
#    public = models.BooleanField(default=False)
#    owner = models.ManyToManyField(User, related_name='owned_collections')
#    editors = models.ManyToManyField(User, related_name='editable_collections')
#    viewer = models.ManyToManyField(User, related_name='subscribed_collections')

def defaultData():
    iso ,c = RegistrationAuthority.objects.get_or_create(
                name="ISO/IEC",description="ISO/IEC")
    iso_wg,c = Workgroup.objects.get_or_create(name="ISO/IEC Workgroup")
    iso_package,c = Package.objects.get_or_create(
        name="ISO/IEC 11404 DataTypes",
        description="A collection of datatypes as described in the ISO/IEC 11404 Datatypes standard",
        workgroup=iso_wg)
    iso.register(iso_package,STATES.standard,timezone.now())
    dataTypes = [
       ("Boolean","A binary value expressed using a string (e.g. true or false)."),
       ("Currency","A numeric value expressed using a particular medium of exchange."),
       ("Date/Time","A specific instance of time expressed in numeric form."),
       ("Number","A sequence of numeric characters which may contain decimals, excluding codes with 'leading' characters e.g. '01','02','03'. "),
       ("String","A sequence of alphabetic and/or numeric characters, including 'leading' characters e.g. '01','02','03'."),
       ]
    for name,desc in dataTypes:
        dt,created = DataType.objects.get_or_create(name=name,description=desc,workgroup=iso_wg)
        iso.register(dt,STATES.standard,datetime.date(2000,1,1))
        iso_package.items.add(dt)
        print "making datatype: {name}".format(name=name)
    reprClasses = [
       ("Code","A system of valid symbols that substitute for specified values e.g. alpha, numeric, symbols and/or combinations."),
       ("Count","Non-monetary numeric value arrived at by counting."),
       ("Currency","Monetary representation."),
       ("Date","Calendar representation e.g. YYYY-MM-DD"),
       ("Graphic","Diagrams, graphs, mathematical curves, or the like . usually a vector image."),
       ("Icon","A sign or representation that stands for its object by virtue of a resemblance or analogy to it."),
       ("Picture","A visual representation of a person, object, or scene - usually a raster image."),
       ("Quantity","A continuous number such as the linear dimensions, capacity/amount (non-monetary) of an object."),
       ("Text","A text field that is usually unformatted."),
       ("Time","Time of day or duration eg HH:MM:SS.SSSS."),
       ]
    for name,desc in reprClasses:
        rc,created = RepresentationClass.objects.get_or_create(name=name,description=desc)
        print "making representation class: {name}".format(name=name)
    unitsOfMeasure = [
        ("Length", [
         ("Centimetre", "cm"),
         ("Millimetre", "mm"),
        ]),
        ("Temperature", [
         ("Degree", "Celsius"),
        ]),
        ("Time", [
         ("Second", "s"),
         ("Minute", "min"),
         ("Hour", "h"),
         ("Hour and minute", ""),
         ("Day", "D"),
         ("Week", ""),
         ("Year", "Y"),
        ]),
        ("Weight", [
         ("Gram", "g"),
         ("Kilogram", "Kg"),
        ]),
    ]
    for measure,units in unitsOfMeasure:
        m,created = Measure.objects.get_or_create(name=measure,description="")
        print "making measure: {name}".format(name=name)
        for name,symbol in units:
            u,created = UnitOfMeasure.objects.get_or_create(name=name,symbol=symbol,measure=m)
            print "   making unit of measure: {name}".format(name=name)


def favourite_updated(recipient,obj):
    notify.send(recipient, recipient=recipient, verb="changed a favourited item", target=obj)
def workgroup_item_updated(recipient,obj):
    notify.send(recipient, recipient=recipient, verb="changed a item in the workgroup", target=obj)
def workgroup_item_new(recipient,obj):
    notify.send(recipient, recipient=recipient, verb="a new item in the workgroup", target=obj)
@receiver(post_save)
def concept_saved(sender, instance, created, **kwargs):
    if not issubclass(sender, _concept):
        return
    for p in instance.favourited_by.all():
        favourite_updated(recipient=p.user,obj=instance)
    for user in instance.workgroup.viewers:
        if created:
            workgroup_item_new(recipient=user,obj=instance)
        else:
            workgroup_item_updated(recipient=user,obj=instance)
    try:
        # This will fail during first load, and if admins delete aristotle.
        system = User.objects.get(username="aristotle")
        for post in instance.relatedDiscussions.all():
            DiscussionComment.objects.create(
                post = post,
                body = 'The item "{name}" (id:{iid}) has been changed.\n\n\
                    <a href="{url}">View it on the main site.</a>.'.format(
                    name=instance.name,
                    iid = instance.id,
                    url = reverse("aristotle:item",args=[instance.id])
                ),
                author = system,
            )
    except:
        pass
@receiver(post_save,sender=DiscussionComment)
def new_comment_created(sender, **kwargs):

    comment = kwargs['instance']
    post = comment.post
    if not kwargs['created']:
        return # We don't need to notify a topic poster of an edit.
    if comment.author == post.author:
        return # We don't need to tell someone they replied to themselves
    notify.send(comment.author, recipient=post.author, verb="made a comment on your post", target=post)

# Loads test bed of data
def testData():
    defaultData()
    print "configuring users"

    if not User.objects.filter(username__iexact='possum').first():
        user = User.objects.create_superuser('possum','','pilches')
        print "making superuser"

    #Set up based workgroup and workers
    pw,c = Workgroup.objects.get_or_create(name="Possum Workgroup")
    users = [('vicky','Viewer'),
             ('eddie','Editor'),
             ('mandy','Manager'),
             ('sally','Super-Editor'),
            ]
    for name,role in users:
        user = User.objects.filter(username__iexact=name).first()
        if not user:
            user = User.objects.create_user(name,'',role)
            print "making user: {name}".format(name=name)
        user.first_name=name.title()
        user.last_name=role
        print "updated user's name to {fn} {ln}".format(fn=user.first_name,ln=user.last_name)
        user.profile.workgroups.add(pw)
        pw.giveRoleToUser(role,user)
        user.save()

    oldoc,c  = ObjectClass.objects.get_or_create(name="Person",
            workgroup=pw,description="A human being, whether man or woman.")
    oc,c  = ObjectClass.objects.get_or_create(name="Person",
            workgroup=pw,description="A human being, whether man, woman or child.")
    oc.synonyms = "People"
    oc.readyToReview = True
    oc.save()
    oldoc.superseded_by = oc
    oldoc.save()
    p,c   = Property.objects.get_or_create(name="Age",
            workgroup=pw,description="The length of life or existence.")
    dec,c = DataElementConcept.objects.get_or_create(name="Person-Age",
            workgroup=pw,description="The age of the person.",
            objectClass=oc,property=p
            )
    dec,c = DataElementConcept.objects.get_or_create(name="Person-Age",
            workgroup=pw,description="The age of the person.",
            objectClass=oc,property=p
            )
    W,c   = Property.objects.get_or_create(name="Weight",
            workgroup=pw,description="The weight of an object.")
    H,c   = Property.objects.get_or_create(name="Height",
            workgroup=pw,description="The height of an object, usually measured from the ground to its highest point.")
    WW,c = DataElementConcept.objects.get_or_create(name="Person-Weight",
            workgroup=pw,description="The weight of the person.",
            objectClass=oc,property=W
            )
    HH,c = DataElementConcept.objects.get_or_create(name="Person-Height",
            workgroup=pw,description="The height of the person.",
            objectClass=oc,property=H
            )

    vd,c   = ValueDomain.objects.get_or_create(name="Total years N[NN]",
            workgroup=pw,description="Total number of completed years.",
            format = "X[XX]" ,
            maximumLength = 3,
            unitOfMeasure = UnitOfMeasure.objects.filter(name__iexact='Week').first(),
            dataType = DataType.objects.filter(name__iexact='Number').first(),
            )
    de,c = DataElement.objects.get_or_create(name="Person-age, total years N[NN]",
            workgroup=pw,description="The age of the person in (completed) years at a specific point in time.",
            dataElementConcept=dec,valueDomain=vd
            )
    p,c   = Property.objects.get_or_create(name="Sex",
            workgroup=pw,description="A gender.")
    dec,c = DataElementConcept.objects.get_or_create(name="Person-Sex",
            workgroup=pw,description="The sex of the person.",
            objectClass=oc,property=p
            )
    vd,c   = ValueDomain.objects.get_or_create(name="Sex Code",
            workgroup=pw,description="A code for sex.",
            format = "X" ,
            maximumLength = 3,
            unitOfMeasure = UnitOfMeasure.objects.filter(name__iexact='Week').first(),
            dataType = DataType.objects.filter(name__iexact='Number').first(),
            )
    for val,mean in [(1,'Male'),(2,'Female')]:
        codeVal = PermissibleValue(value=val,meaning=mean,valueDomain=vd,order=1)
        codeVal.save()
    de,c = DataElement.objects.get_or_create(name="Person-sex, Code N",
            workgroup=pw,description="The sex of the person with a code.",
            )
    de.dataElementConcept=dec
    de.valueDomain=vd
    de.save()

    print "Configuring registration authority"
    ra,c = RegistrationAuthority.objects.get_or_create(
                name="Welfare",description="Welfare Authority")#,workflow=wf)
    ra,c = RegistrationAuthority.objects.get_or_create(
                name="Health",description="Health Authority")#,workflow=wf)
    users = [('reggie','Registrar'),
            ]
    pw.registrationAuthorities.add(ra)
    pw.save()
    for name,role in users:
        user = User.objects.filter(username__iexact=name).first()
        if not user:
            user = User.objects.create_user(name,'',role)
            print "making user: {name}".format(name=name)
        user.first_name=name.title()
        user.last_name=role
        user.profile.registrationAuthorities.add(ra)
        ra.giveRoleToUser(role,user)
        user.save()

    #Lets register a thing :/
    reg,c = Status.objects.get_or_create(
            concept=oc,
            registrationAuthority=ra,
            registrationDate = datetime.date(2009,04,28),
            state =  STATES.standard
            )
