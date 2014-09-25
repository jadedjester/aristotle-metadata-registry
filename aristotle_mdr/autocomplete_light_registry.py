import autocomplete_light
from aristotle_mdr import models as MDR

autocompleteTemplate = {
    # Just like in ModelAdmin.search_fields
    'name':'AutocompleteConcept',
    'choice_template':"aristotle_mdr/actions/autocompleteItem.html",
    'attr':{
        # This will set the input placeholder attribute:
        'placeholder': 'Other model name ?',
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 2,
    },
    # This will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.Widget.maximumValues (jQuery handles the naming
    # conversion).
    'widget_attrs':{
        #'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        #'class': 'modern-style',
    },
}

class PermissionsAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields=['name', 'description','id']

    def choices_for_request(self):
        self.choices = self.choices.editable_slow(self.request.user)
        return super(PermissionsAutocomplete, self).choices_for_request()

autocompletesToRegister = [
        MDR._concept,
        MDR.DataElement,
        MDR.DataElementConcept,
        MDR.ObjectClass,
        MDR.Property,
        MDR.ValueDomain,
        MDR.DataElementConcept,
        MDR.DataType,
    ]
for cls in autocompletesToRegister:
    # This will generate a PersonAutocomplete class
    x = autocompleteTemplate.copy()
    x['name']='Autocomplete'+cls.__name__
    autocomplete_light.register(cls,PermissionsAutocomplete,**x)

