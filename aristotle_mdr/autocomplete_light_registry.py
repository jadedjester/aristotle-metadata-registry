import autocomplete_light
import aristotle_mdr.models as MDR
from django.contrib.auth.models import User

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

class UserAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields=['first_name', 'last_name','username','email']

u = autocompleteTemplate.copy()
u['name']='Autocomplete_AristotleUser'
u['choice_template']='aristotle_mdr/actions/autocompleteUser.html'
autocomplete_light.register(User,UserAutocomplete,**u)

class PermissionsAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields=['name', 'description','id']

    def choices_for_request(self):
        self.choices = self.choices.visible(self.request.user)
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
        MDR.GlossaryItem,
    ]
for cls in autocompletesToRegister:
    # This will generate a PersonAutocomplete class
    x = autocompleteTemplate.copy()
    x['name']='Autocomplete'+cls.__name__
    autocomplete_light.register(cls,PermissionsAutocomplete,**x)

