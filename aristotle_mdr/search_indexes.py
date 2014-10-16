import datetime
from haystack import indexes
from haystack.query import SearchQuerySet

import models

class baseObjectIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    modified = indexes.DateTimeField(model_attr='modified')
    created = indexes.DateTimeField(model_attr='created')
    name = indexes.CharField(model_attr='name',boost=1)
    #access = indexes.MultiValueField()

    def get_model(self):
        return models.baseAristotleObject

    # From http://unfoldthat.com/2011/05/05/search-with-row-level-permissions.html
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""

        return self.get_model().objects.filter(modified__lte=datetime.datetime.now())

    #def have_access(self, obj):
    #    for user in obj.viewers.users():
    #        yield user

    #    for group in obj.viewers.groups():
    #        yield group

    #def prepare_access(self, obj):
    #    def _access_iter(obj):
    #        have_access = self.have_access(obj)
    #
    #        for obj in have_access:
    #            if isinstance(obj, User):
    #                yield 'user_%i' % obj.id
    #            elif isinstance(obj, Group):
    #                yield 'group_%i' % obj.id
    #
    #    return list(_access_iter(obj))

class conceptIndex(baseObjectIndex):
    statuses = indexes.MultiValueField()
    highest_state = indexes.IntegerField()
    ra_statuses = indexes.MultiValueField()
    registrationAuthorities = indexes.MultiValueField()
    workgroup = indexes.CharField(model_attr="workgroup")
    is_public = indexes.BooleanField()
    version = indexes.CharField(model_attr="version")

    def prepare_registrationAuthorities (self, obj):
        ras = [s.registrationAuthority.id for s in obj.statuses.all()]
        return ras

    def prepare_is_public(self,obj):
        return obj.is_public()

    def prepare_statuses(self, obj):
        # We don't remove duplicates as it should mean the more standard it is the higher it will rank
        states = [s.state_name for s in obj.statuses.all()]
        return states

    def prepare_highest_state(self, obj):
        # Include -99, so "unregistered" items get a value
        state = max([int(s.state) for s in obj.statuses.all()]+[-99])
        """
        We don't want retired or superseded ranking higher than standards during search
        as these are no longer "fit for purpose" so we'll place them below other
        states for the purposes of sorting in search.
        """
        if state == models.STATES.retired:
            state = -10
        elif state == models.STATES.superseded:
            state = -9
        return state


    def prepare_ra_statuses(self, obj):
        # This allows us to check a registration authority and a state simultaneously
        states = ["%s___%s"%(str(s.registrationAuthority.id),str(s.state))
                    for s in obj.statuses.all()]
        return states
    """
    def get_model(self):
        return models.managedObject
    """
class ObjectClassIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.ObjectClass

class PropertyIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.Property

class PackageIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.Package

class DataElementConceptIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.DataElementConcept

class DataElementIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.DataElement

class ValueDomainIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.ValueDomain
