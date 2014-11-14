import autocomplete_light
autocomplete_light.autodiscover()

from django import forms
from django.utils.translation import ugettext_lazy as _

import aristotle_mdr.models as MDR
import aristotle_mdr.widgets as widgets
from aristotle_mdr.perms import user_can_edit
from aristotle_mdr.utils import concept_to_clone_dict

def MembershipField(model,name):
    from django.contrib.admin.widgets import FilteredSelectMultiple
    return forms.ModelMultipleChoiceField(
        queryset=model.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(name, False)
        )

class AristotleProfileForm(forms.ModelForm):
    steward_in = MembershipField(MDR.Workgroup,_('workgroups'))
    submitter_in = MembershipField(MDR.Workgroup,_('workgroups'))
    viewer_in = MembershipField(MDR.Workgroup,_('workgroups'))
    workgroup_manager_in = MembershipField(MDR.Workgroup,_('workgroups'))

    registrationauthority_manager_in = MembershipField(MDR.RegistrationAuthority,'registration authorities')
    registrar_in = MembershipField(MDR.RegistrationAuthority,_('registration authorities'))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AristotleProfileForm, self).__init__(*args, **kwargs)
        from django.contrib.auth.models import User # paranoid about circular imports now

        #if self.instance and self.instance.user.count() == 1: # and self.instance.user.exists():
        try:
            self.fields['registrar_in'].initial = self.instance.user.registrar_in.all()
            self.fields['registrationauthority_manager_in'].initial = self.instance.user.registrationauthority_manager_in.all()

            self.fields['workgroup_manager_in'].initial = self.instance.user.workgroup_manager_in.all()
            self.fields['steward_in'].initial = self.instance.user.steward_in.all()
            self.fields['submitter_in'].initial = self.instance.user.submitter_in.all()
            self.fields['viewer_in'].initial = self.instance.user.viewer_in.all()
        except User.DoesNotExist:
            pass


    def save_memberships(self, *args, **kwargs):
        self.instance.user.steward_in = self.cleaned_data['steward_in']
        self.instance.user.registrar_in = self.cleaned_data['registrar_in']

class AdminConceptForm(forms.ModelForm):
    # Thanks: http://stackoverflow.com/questions/6034047/one-to-many-inline-select-with-django-admin
    # Although concept is an abstract class, we still need this to have a reverse one-to-many edit field.
    class Meta:
        model = MDR._concept

    deprecated = forms.ModelMultipleChoiceField(queryset=MDR._concept.objects.all())

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        auto_fields = kwargs.pop('auto_fields', None)
        clone = self.request.GET.get("clone",None)
        name_suggest_fields = kwargs.pop('name_suggest_fields',[])
        separator = kwargs.pop('separator','-')
        if clone:
            item_to_clone = MDR._concept.objects.filter(id=clone).first().item
            kwargs['initial'] = concept_to_clone_dict(item_to_clone)

        super(AdminConceptForm, self).__init__(*args, **kwargs)
        if self.instance and not clone:
            self.itemtype = self.instance.__class__
            self.fields['deprecated'] = forms.ModelMultipleChoiceField(
                    required=False,
                    label="Supersedes",
                    queryset=self.itemtype.objects.all(),
                    widget=autocomplete_light.MultipleChoiceWidget(self.instance.get_autocomplete_name())
                )
            self.fields['deprecated'].initial = self.instance.supersedes.all()
            self.fields['superseded_by'].widget = autocomplete_light.ChoiceWidget(self.instance.get_autocomplete_name())

        if name_suggest_fields:
            self.fields['name'].widget = widgets.NameSuggestInput(name_suggest_fields=name_suggest_fields,separator=separator)

        if auto_fields:
            for f,l in auto_fields['fk']:
                self.fields[f].widget = autocomplete_light.ChoiceWidget(l.get_autocomplete_name())


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
