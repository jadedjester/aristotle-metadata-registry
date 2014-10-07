from django.forms.widgets import RendererMixin,CheckboxSelectMultiple,ChoiceFieldRenderer,SelectMultiple,ChoiceInput,CheckboxChoiceInput, CheckboxFieldRenderer,SubWidget
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class BootstrapChoiceInput(CheckboxChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        return format_html('{1}<label{0}> <span>{2}</span></label>', label_for, self.tag(), self.choice_label)

class BootstrapCheckboxFieldRenderer(CheckboxFieldRenderer):
    """
    An object used by RadioSelect to enable customization of radio widgets.
    """
    choice_input_class = BootstrapChoiceInput

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id', None)
        start_tag = format_html('<ul id="{0}" class="dropdown-menu" role="menu">', id_) if id_ else '<ul class="dropdown-menu" role="menu">'
        output = [start_tag]
        for widget in self:
            output.append(format_html('<li>{0}</li>', force_text(widget)))
        output.append('</ul>')
        return mark_safe('\n'.join(output))
"""
# This might replace the above for Django 1.7
class BootstrapCheckboxFieldRenderer(ChoiceFieldRenderer):
    outer_html = '<h1>What?</h1><ul{id_attr} class="dropdown-menu" role="menu">{content}</ul>'
    choice_input_class = CheckboxChoiceInput
""" 

class BootstrapDropdownCheckboxWidget(CheckboxSelectMultiple):
    renderer = BootstrapCheckboxFieldRenderer