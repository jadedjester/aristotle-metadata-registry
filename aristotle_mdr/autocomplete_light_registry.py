import autocomplete_light
from aristotle_mdr import models as MDR

# This will generate a PersonAutocomplete class
autocomplete_light.register(MDR.DataElement,
    # Just like in ModelAdmin.search_fields
    name='AutocompleteDataElement',
    #choice_html_format="aristotle_mdr/actions/autocompleteItem.html",
    search_fields=['^name', 'description'],
    attrs={
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
    widget_attrs={
        #'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        #'class': 'modern-style',
    },
)

