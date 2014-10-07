{% comment %}

{% endcomment %}

function(editor) {
    getGlossaryList(); {# initialise the glossary list #}
    var self = $.inplaceeditform;
    setTimeout(function () {
       $('#' + editor.id).parents(self.formSelector).find('.apply').data('editor', editor);
       $('#' + editor.id).parents(self.formSelector).find('.cancel').data('editor', editor);
    }, 300);
    var value = $('#' + editor.id).html();
    var form = $('#' + editor.id).parents(self.formSelector);
    {% ifequal autosave '1' %}
        editor.on('blur', function () {
            if (editor.isDirty()) {
                self.methods.bind(self.methods.autoSaveCallBack, {'oldValue': value,
                                                                  'tag': $('#' + editor.id)})();
            } else {
                form.find('.cancel').click();
            }
        });
    {% else %}
        editor.on('blur', function () {
            return false;
        });
    {% endifequal %}

    editor.addButton('save', {
        title : 'Save changes',
        classes: 'widget btn aristotle-icon aristotle-save',
        text: 'Save',
        onclick: function() {
            if (form.data('ajaxTime')) {
                return;
            }
            form.find('.apply').click();
        }
    });
    editor.addButton('cancel', {
        title : 'Cancel and discard changes',
        classes: 'widget btn aristotle-icon aristotle-cancel',
        text: 'Cancel',
        onclick: function() {
            if (form.data('ajaxTime')) {
                return;
            }
            form.find('.cancel').click();
        }
    });
    editor.addShortcut('alt+s','save',
        function() {
            if (form.data('ajaxTime')) {
                return;
            }
            form.find('.apply').click();
        });
    editor.addShortcut('alt+c','cancel',
        function() {
            if (form.data('ajaxTime')) {
                return;
            }
            form.find('.cancel').click();
        });

    editor.addButton('glossary', {
        title : 'Insert glossary item',
        text: 'Glossary',
        classes: 'widget btn aristotle-icon aristotle-glossary',
        onclick: function() {
            editor.windowManager.open( {
                title: 'Insert glossary item',
                body: [{
                    type: 'listbox',
                    name: 'term',
                    label: 'Select a term',
                    'values':getGlossaryList()
                },
                {
                    type: 'textbox',
                    name: 'text',
                    label: 'Link text (leave blank to use to the glossary name)'
                }],
                onsubmit: function( e ) {
                    i = e.data.term;
                    text = e.data.text || glossaryLookup[i].name;
                    editor.insertContent( '<a class="aristotle_glossary" data-aristotle_glossary_id="'+i+'" href="'+glossaryLookup[i].url+'">' + text + '</a>');
                }
            });
        }
    });

}
