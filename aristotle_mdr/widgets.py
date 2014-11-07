from django.forms.widgets import TextInput,CheckboxSelectMultiple,ChoiceFieldRenderer,ChoiceInput,CheckboxChoiceInput, RadioSelect
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class NameSuggestInput(TextInput):
    def __init__(self, *args, **kwargs):
        self.suggests = kwargs.pop('name_suggest_fields')
        self.separator = kwargs.pop('separator','-')
        super(NameSuggestInput, self).__init__(*args, **kwargs)
    def render(self, name, value, attrs=None):
        out = super(NameSuggestInput, self).render(name, value, attrs)
        if self.suggests:
            button = u"<button type='button' data-separator='{}' data-suggest-fields='{}'>Suggest</button>".format(self.separator,",".join(self.suggests))
            out = u"<div class='suggest_name_wrapper'>{}{}</div>".format(out,button)
        return mark_safe(out)


class BootstrapChoiceInput(ChoiceInput):
    input_type = 'radio'

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        return format_html('{1}<label{0} role="menuitem" tabindex="-1"> <span>{2}</span></label>', label_for, self.tag(), self.choice_label)
    def tag(self):
        self.attrs['tabindex'] = -1
        return super(BootstrapChoiceInput,self).tag()

class BootstrapCheckInput(BootstrapChoiceInput,CheckboxChoiceInput):
    input_type = 'checkbox'

class BootstrapChoiceFieldRenderer(ChoiceFieldRenderer):
    wrap = True
    choice_input_class = BootstrapChoiceInput

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id', None)
        output=[]
        for widget in self:
            output.append(format_html('<li role="presentation">{0}</li>', force_text(widget)))
        if self.wrap:
            start_tag = format_html('<ul id="{0}" class="dropdown-menu" role="menu">', id_) if id_ else '<ul class="dropdown-menu" role="menu">'
            output = [start_tag]+output
            output.append('</ul>')
        return mark_safe('\n'.join(output))

class BootstrapCheckboxFieldRenderer(BootstrapChoiceFieldRenderer):
    choice_input_class = BootstrapCheckInput

class BootstrapRadioFieldRenderer(BootstrapChoiceFieldRenderer):
    choice_input_class = BootstrapChoiceInput

class BootstrapIntelligentDateRenderer(BootstrapChoiceFieldRenderer):
    choice_input_class = BootstrapChoiceInput
    wrap = False

class BootstrapDropdownSelect(RadioSelect):
    renderer = BootstrapRadioFieldRenderer
    allow_multiple_selected = False

class BootstrapDropdownIntelligentDate(BootstrapDropdownSelect):
    renderer = BootstrapIntelligentDateRenderer

class BootstrapDropdownSelectMultiple(CheckboxSelectMultiple):
    renderer = BootstrapCheckboxFieldRenderer
    allow_multiple_selected = True