import autocomplete_light
autocomplete_light.autodiscover()

from django import forms
import aristotle_mdr.models as MDR # Treble-one seven nine
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from django.contrib.admin import widgets

from haystack.forms import ModelSearchForm
from aristotle_mdr.perms import user_can_view, user_can_edit
from django.utils.safestring import mark_safe
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils import timezone
from django.forms import model_to_dict

class AdminConceptForm(forms.ModelForm):
    # Thanks: http://stackoverflow.com/questions/6034047/one-to-many-inline-select-with-django-admin
    class Meta:
        model = MDR._concept

    deprecated = forms.ModelMultipleChoiceField(queryset=MDR._concept.objects.all())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        clone = self.request.GET.get("clone",None)
        if clone:
            clone = MDR._concept.objects.filter(id=clone).first()
            #clone.pop('id') # Get rid of the id.
            #clone['name'] = "sdfsdfsdfsdf  "+str(clone)
            kwargs['initial']=model_to_dict(clone)
        super(AdminConceptForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.itemtype = self.instance.__class__
            self.fields['deprecated'] = forms.ModelMultipleChoiceField(
                    required=False,
                    label="Supersedes",
                    queryset=self.itemtype.objects.all(),
                    widget=widgets.FilteredSelectMultiple("items to supersede",True)
                )
            self.fields['deprecated'].initial = self.instance.supersedes.all()

    def save_model(self, *args, **kwargs):
        instance = super(AdminConceptForm, self).save_model(*args, **kwargs)
        request = kwargs['request']
        for i in instance.supersedes.all():
            if user_can_edit(request.user,i) and i not in self.cleaned_data['deprecated']:
                instance.supersedes.remove(i)
        for i in self.cleaned_data['deprecated']:
            if user_can_edit(request.user,i): #Would check item.supersedes but its a set
                instance.supersedes.add(i)

        return instance

class ConceptForm(forms.ModelForm):
    """
    Add this in when we look at reintroducing the fancy templates.
    required_css_class = 'required'
    """
    def __init__(self, *args, **kwargs):
        #TODO: Have tis throw a 'no user' error
        self.user = kwargs.pop('user', None)
        super(ConceptForm, self).__init__(*args, **kwargs)
        if not self.user.is_superuser:
            self.fields['workgroup'].queryset = self.user.profile.workgroups

    pass
#    userAware = forms.BooleanField()
#
#    def __init__(self, *args, **kwargs):
#        hasSimilarItems = kwargs.get('hasSimilarItems', False)
#        if 'hasSimilarItems' in kwargs:
#            del kwargs['hasSimilarItems']
#        super(ConceptForm, self).__init__(*args, **kwargs)
#        if hasSimilarItems:
#            del self.fields['userAware']

class ValueDomainForm(ConceptForm):
    template = "aristotle_mdr/create/valueDomain.html"

    class Meta:
        model = MDR.ValueDomain
        exclude = ['readyToReview','superseded_by']

class DataElementConceptForm(ConceptForm):
    template = "aristotle_mdr/create/dataElementConcept.html"

    class Meta:
        model = MDR.DataElementConcept
        exclude = ['readyToReview','superseded_by']

class PropertyForm(ConceptForm):
    template = "aristotle_mdr/create/property.html"

    class Meta:
        model = MDR.Property
        exclude = ['readyToReview','superseded_by']

class ObjectClassForm(ConceptForm):
    template = "aristotle_mdr/create/objectClass.html"

    class Meta:
        model = MDR.ObjectClass
        exclude = ['readyToReview','superseded_by']

class UserSelfEditForm(forms.Form):
    template = "aristotle_mdr/userEdit.html"

    first_name      = forms.CharField(required=False,label=u'First Name')
    last_name       = forms.CharField(required=False,label=u'Last Name')
    email           = forms.EmailField(required=False,label=u'Email Address')


# For stating that an item deprecates other items.
class DeprecateForm(forms.Form):
    olderItems = forms.ModelMultipleChoiceField(
                queryset=MDR._concept.objects.all(),
                label="Deprecate items",
                widget=autocomplete_light.MultipleChoiceWidget('AutocompleteDataElement'))

                #widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.qs = kwargs.pop('qs')
        super(DeprecateForm, self).__init__(*args, **kwargs)
        self.fields['olderItems']=forms.ModelMultipleChoiceField(
                queryset=self.qs,
                label="Deprecate items",
                #widget=forms.CheckboxSelectMultiple,
                initial=self.item.supersedes.all(),
                widget=autocomplete_light.MultipleChoiceWidget('AutocompleteDataElement'))


# For superseding an item with a newer one.
class SupersedeForm(forms.Form):
    newerItem = forms.ModelChoiceField(
                queryset=MDR._concept.objects.all(),
                empty_label="None",
                label="Superseded by")
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.qs = kwargs.pop('qs')
        super(SupersedeForm, self).__init__(*args, **kwargs)
        self.fields['newerItem']=forms.ModelChoiceField(
                queryset=self.qs,
                empty_label="None",
                label="Superseded by",
                initial=self.item.superseded_by)

class ChangeStatusForm(forms.Form):
    state = forms.ChoiceField(choices=MDR.STATES,widget=forms.RadioSelect)
    registrationDate = forms.DateField(
        required=False,label="Registration date",
        widget=DateTimePicker(options={"format": "YYYY-MM-DD"}),
        initial=timezone.now()
        )
    cascadeRegistration = forms.ChoiceField(initial=False,
        choices=[(0,'No'),(1,'Yes')],
        label="Do you want to update the registration of associated items?"
    )
    # Thanks to http://jacobian.org/writing/dynamic-form-generation/
    def __init__(self, *args, **kwargs):
        ras = kwargs.pop('ras')
        super(ChangeStatusForm, self).__init__(*args, **kwargs)
        raChoices = [(ra.id,ra.name) for ra in ras]
        self.fields['registrationAuthorities']=forms.MultipleChoiceField(
                label="Registration Authorities",
                choices=raChoices,
                widget=forms.CheckboxSelectMultiple)

    def clean_cascadeRegistration(self):
        return self.cleaned_data['cascadeRegistration'] == "1"

    def clean_state(self):
        state = self.cleaned_data['state']
        try:
            state = int(state)
            MDR.STATES[state]
        except ValueError, IndexError:
            # state is either not a string or not a valid STATE, so raise an error
            # Any other errors will be thrown accordingly
            raise forms.ValidationError("Please select a valid status.")
        return state


class AddWorkgroupMembers(forms.Form):
    roles = forms.MultipleChoiceField(
            label="Workgroup roles",
            choices=zip(sorted(MDR.Workgroup.roles.keys()),sorted(MDR.Workgroup.roles.keys())),
            widget=forms.CheckboxSelectMultiple
            )
    users = forms.MultipleChoiceField(
            label="Select users",
            choices=[(user.id,"%s %s (%s)"%(user.first_name,user.last_name,user.username)) for user in User.objects.all()],
            widget=forms.CheckboxSelectMultiple
            )

    def clean_roles(self):
        roles = self.cleaned_data['roles']
        roles = [role for role in roles if role in MDR.Workgroup.roles.keys()]
        return roles

    def clean_users(self):
        users = self.cleaned_data['users']
        return User.objects.filter(id__in=users)

# Thanks http://stackoverflow.com/questions/6958708/grappelli-to-hide-sortable-field-in-inline-sortable-django-admin
class PermissibleValueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermissibleValueForm, self).__init__(*args, **kwargs)
        self.fields['order'].widget = forms.HiddenInput()
    class Meta:
        model = MDR.PermissibleValue


class DEC_Initial_Search(forms.Form):
    template = "aristotle_mdr/create/dec_1_initial_search.html"
    # Object class fields
    oc_name = forms.CharField(max_length=100)
    oc_desc = forms.CharField(widget = forms.Textarea,required=False)
    # Property fields
    pr_name = forms.CharField(max_length=100)
    pr_desc = forms.CharField(widget = forms.Textarea,required=False)

class DEC_Results(forms.Form):
    def __init__(self, oc_results=None, pr_results=None , *args, **kwargs):
        super(DEC_Results, self).__init__(*args, **kwargs)

        # If we are passed a
        if oc_results:
            oc_options = []
            for oc in oc_results:
                # TODO: THIS IS A BAAAAD CHOICE, BUT WE'LL ACCEPT IT FOR NOW!!!
                # HTML in code is a BAD IDEA... but we accept it here because we need
                # links on the options for users to preview the possible options.
                label = mark_safe('<a href="/item/{id}">{name}</a>'.format(id=oc.id,name=oc.name))
                oc_options.append((oc.id,label))
            oc_options.append(("X","None of the above meet my needs"))
            oc_options=tuple(oc_options)
            self.fields['oc_options'] = forms.ChoiceField(verbose_name="Similar Object Classes",
                                        choices=oc_options, widget=forms.RadioSelect())


class PermissionSearchForm(ModelSearchForm):
    """
        We need to make a new form as permissions to view objects are few finicky.
        This form allows us to perform the base query then restrict it to just those
        of interest.

        TODO: This might not scale well, so it may need to be looked at in production.
    """
    startDate = forms.DateField(required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime": False}),
        )
    endDate = forms.DateField(required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime": False}),
        )
    # Use short singular names as they look more semantic in the URL.
    ras = [(ra.id, ra.name) for ra in MDR.RegistrationAuthority.objects.all()]
    ra = forms.MultipleChoiceField(required=False,
        choices=ras,widget=forms.CheckboxSelectMultiple)
    state = forms.MultipleChoiceField(required=False,
        choices=MDR.STATES,widget=forms.CheckboxSelectMultiple)
    public_only = forms.BooleanField(required=False,
        label="public items"
    )
    myWorkgroups_only = forms.BooleanField(required=False,
        label="items in my workgroups"
    )

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PermissionSearchForm, self).search()

        #Whoosh workaround
        if self.get_models():
            for model in ['%s.%s'%(m._meta.app_label,m._meta.object_name) for m in self.get_models()]:
                sqs = sqs.filter_or(django_ct=model)

        if not self.is_valid():
            return self.no_query_found()

        user = self.request.user

        if self.cleaned_data['state']:
            states = [MDR.STATES[int(s)] for s in self.cleaned_data['state']]
            sqs = sqs.filter(statuses__in=states)
        if self.cleaned_data['ra']:
            ras = [ra for ra in self.cleaned_data['ra']]
            sqs = sqs.filter(registrationAuthorities__in=ras)


        if user.is_anonymous():
            # Regular users can only see public items, so boot them off now.
            return sqs.filter(is_public=True)

        public_only=False
        if self.cleaned_data['public_only']:
            public_only = "on" == self.cleaned_data['public_only']
            sqs = sqs.filter(is_public=True)
        myWorkgroups_only=False
        if self.cleaned_data['myWorkgroups_only']:
            myWorkgroups_only = "on" == self.cleaned_data['myWorkgroups_only']
            # Restricted it to only workgroups as if a superuser want to search everything they can just not tick this box
            sqs = sqs.filter(workgroup__in=user.profile.workgroups.all())

        if not public_only or not myWorkgroups_only:
            # If its public or in a users workgroup they can see it so, we don't need to restrict the query any further. This will (should?) save time on the search.
            # Can't use a generator or we would.
            sqs = [s for s in sqs] # if user_can_view(user,s.object)]

        return sqs

