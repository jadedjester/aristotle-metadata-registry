from inplaceeditform_extra_fields.fields import AdaptorTinyMCEField
from inplaceeditform_extra_fields.widgets import TinyMCE
from inplaceeditform.fields import AdaptorChoicesField
from inplaceeditform.commons import apply_filters

from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.forms.extras import widgets

conf = dict(
    toolbar=("save cancel | undo redo | bold italic | "
             "subscript superscript | " #spellchecker | "
             "bullist numlist | link image"),
    #plugins= "spellchecker",
    menubar=False)

class AristotleRichTextField(AdaptorTinyMCEField):
    @property
    def name(self):
        return 'aristotlerichtextfield'

    @property
    def TinyMCE(self):
        return AristotleTinyMCE

class AristotleTinyMCE(TinyMCE):
    def __init__(self, extra_mce_settings=None,
                 config=None, width=None, *args, **kwargs):
        super(AristotleTinyMCE, self).__init__(extra_mce_settings=conf,*args, **kwargs)
        self.mce_settings['setup'] = ''.join(render_to_string('aristotle_mdr/tinymce/setup.js', config).splitlines())

class booleanYesNo(AdaptorChoicesField):
    def __init__(self, *args, **kwargs):
        super(booleanYesNo, self).__init__(*args, **kwargs)

    def get_field(self):
        field = super(booleanYesNo, self).get_field()
        field.field.widget = widgets.Select(choices=((True, _('Yes')),(False, _('No'))))
        return field

    def render_value(self, field_name=None):
        field_name = field_name or self.field_name_render
        value = getattr(self.obj, field_name)
        if value:
            value = _("Yes")
        else:
            value = _("No")
        return apply_filters(value, self.filters_to_show, self.loads)

