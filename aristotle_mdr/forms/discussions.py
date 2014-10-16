import autocomplete_light
autocomplete_light.autodiscover()

from django import forms
import aristotle_mdr.models as MDR

class NewPostForm(forms.ModelForm):
    relatedItems = forms.ModelMultipleChoiceField(
                queryset=MDR._concept.objects.all(),
                label="Related items",required=False,
                widget=autocomplete_light.MultipleChoiceWidget('Autocomplete_concept'))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['workgroup'].queryset = self.user.profile.myWorkgroups

    class Meta:
        model = MDR.DiscussionPost
        exclude = ['author','closed']

class EditPostForm(forms.ModelForm):
    class Meta:
        model = MDR.DiscussionPost
        exclude = ['author','workgroup','closed']

class CommentForm(forms.ModelForm):
    class Meta:
        model = MDR.DiscussionComment
        exclude = ['author','post']