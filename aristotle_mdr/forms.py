import autocomplete_light
autocomplete_light.autodiscover()

from django import forms
import aristotle_mdr.models as MDR
from django.db.models import Q
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _

from haystack.forms import SearchForm, model_choices
#from haystack.forms import ModelSearchForm, model_choices
from haystack.query import SearchQuerySet
from aristotle_mdr.perms import user_can_view, user_can_edit
from aristotle_mdr.widgets import BootstrapDropdownCheckboxWidget
from django.utils.safestring import mark_safe
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils import timezone
from django.forms import model_to_dict

class AdminConceptForm(forms.ModelForm):
    # Thanks: http://stackoverflow.com/questions/6034047/one-to-many-inline-select-with-django-admin
    # Although concept is an abstract class, we still need this to have a reverse one-to-many edit field.
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
            self.fields['workgroup'].queryset = self.user.profile.myWorkgroups

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

class DiscussionNewPostForm(forms.ModelForm):
    relatedItems = forms.ModelMultipleChoiceField(
                queryset=MDR._concept.objects.all(),
                label="Related items",required=False,
                widget=autocomplete_light.MultipleChoiceWidget('Autocomplete_concept'))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DiscussionNewPostForm, self).__init__(*args, **kwargs)
        self.fields['workgroup'].queryset = self.user.profile.myWorkgroups

    class Meta:
        model = MDR.DiscussionPost
        exclude = ['author','closed']

class DiscussionEditPostForm(forms.ModelForm):
    class Meta:
        model = MDR.DiscussionPost
        exclude = ['author','workgroup','closed']

class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = MDR.DiscussionComment
        exclude = ['author','post']

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
                label="Supersede older items",
                required=False,
                widget=autocomplete_light.MultipleChoiceWidget('Autocomplete_concept'))

                #widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.qs = kwargs.pop('qs')
        self.user = kwargs.pop('user')
        super(DeprecateForm, self).__init__(*args, **kwargs)
        self.fields['olderItems']=forms.ModelMultipleChoiceField(
                queryset=self.qs,
                label="Supersede older items",
                required=False,
                initial=self.item.supersedes.all(),
                widget=autocomplete_light.MultipleChoiceWidget(self.item.get_autocomplete_name()))

    def clean_olderItems(self):
        olderItems = self.cleaned_data['olderItems']
        if self.item in olderItems:
            raise forms.ValidationError("An item may not supersede itself")
        for i in olderItems:
            if not user_can_edit(self.user,i):
                raise forms.ValidationError("You cannot supersede an item that you do not have permission to edit")
        return olderItems

# For superseding an item with a newer one.
class SupersedeForm(forms.Form):
    newerItem = forms.ModelChoiceField(
                queryset=MDR._concept.objects.all(),
                empty_label="None",
                label="Superseded by",
                required=False,
                widget=autocomplete_light.ChoiceWidget('Autocomplete_concept'))
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.qs = kwargs.pop('qs')
        self.user = kwargs.pop('user')
        super(SupersedeForm, self).__init__(*args, **kwargs)
        self.fields['newerItem']=forms.ModelChoiceField(
                queryset=self.qs,
                empty_label="None",
                label="Superseded by",
                initial=self.item.superseded_by,
                required=False,
                widget=autocomplete_light.ChoiceWidget(self.item.get_autocomplete_name()))
    def clean_newerItem(self):
        item  = self.cleaned_data['newerItem']
        if self.item.id == item.id:
            raise forms.ValidationError("An item may not supersede itself")
        if not user_can_edit(self.user,item):
            raise forms.ValidationError("You cannot supersede with an item that you do not have permission to edit")
        return item


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
    users = forms.ModelMultipleChoiceField(
            label="Select users",
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
            )

    def clean_roles(self):
        roles = self.cleaned_data['roles']
        roles = [role for role in roles if role in MDR.Workgroup.roles.keys()]
        return roles


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


#class PermissionSearchForm(ModelSearchForm):
class PermissionSearchForm(SearchForm):
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
    models = forms.MultipleChoiceField(choices=model_choices(),
                required=False, label=_('Search In'),
                widget=BootstrapDropdownCheckboxWidget
                )

    def search(self,repeat_search=False):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PermissionSearchForm, self).search()

        #Whoosh workaround
        #if self.get_models():
        #    for model in ['%s.%s'%(m._meta.app_label,m._meta.object_name) for m in self.get_models()]:
        #        sqs = sqs.filter_or(django_ct=model)

        if not self.is_valid():
            return self.no_query_found()
        query_text = self.cleaned_data['q']
        states = self.cleaned_data['state']
        ras = self.cleaned_data['ra']
        has_filter = states or ras
        if has_filter and not query_text:
            # If there is a filter, but no `q`uery then we'll force some results.
            sqs = SearchQuerySet().order_by('-modified')
        if query_text and sqs.count() == 0:
            from urllib import quote_plus
            suggestions = []
            has_suggestions = False
            suggested_query = []
            for token in query_text.split(" "):
                if token: # remove blanks
                    suggestion = SearchQuerySet().spelling_suggestion(token)
                    if suggestion:
                        suggested_query.append(suggestion)
                        has_suggestions = True
                    else:
                        suggested_query.append(token)
                    suggestions.append((token,suggestion))
            self.spelling_suggestions = suggestions
            self.has_spelling_suggestions = has_suggestions
            self.suggested_query = quote_plus(' '.join(suggested_query),safe="")

        user = self.request.user

        if states and not ras:
            states = [MDR.STATES[int(s)] for s in self.cleaned_data['state']]
            sqs = sqs.filter(statuses__in=states)
        elif ras and not states:
            ras = [ra for ra in self.cleaned_data['ra']]
            sqs = sqs.filter(registrationAuthorities__in=ras)
        elif states and ras:
            # If we have both states and ras, merge them so we only search for
            # items with those statuses in those ras
            terms = ["%s___%s"%(str(r),str(s)) for r in ras for s in states]
            sqs = sqs.filter(ra_statuses__in=terms)

        if user.is_anonymous():
            # Regular users can only see public items, so boot them off now.
            return sqs.filter_and(is_public=True)

        q = Q()

        if user.is_superuser:
            pass
        elif not user.profile.is_registrar:
            # Non-registrars can only see public things or things in their workgroup
            q |= Q(workgroup__in=user.profile.workgroups.all())
        elif user.profile.is_registrar:
            q |= Q(workgroup__in=user.profile.workgroups.all())
            q |= Q(registrationAuthorities__in=user.profile.registrarAuthorities)
        else:
            #I'm paranoid...
            q = Q(is_public=True)
            return sqs.filter(q)

        if self.cleaned_data['public_only'] == True:
            q &= Q(is_public=True)
        if self.cleaned_data['myWorkgroups_only'] == True:
            q &= Q(workgroup__in=user.profile.workgroups.all())

        sqs = sqs.filter(q)

        if repeat_search == False and (states or ras) and sqs.count() == 0:
            # If there are 0 results, and filters, lets be nice and remove them.
            # There will be a big message on the search page that says what we did.
            self.cleaned_data['state'] = None
            self.cleaned_data['ra'] = None
            self.auto_broaden_search = True
            sqs = self.search(repeat_search=True)

        return sqs

