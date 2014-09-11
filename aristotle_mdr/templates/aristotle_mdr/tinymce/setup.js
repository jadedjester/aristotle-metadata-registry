function(editor) {
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
        text: 'Save',
        onclick: function() {
            if (form.data('ajaxTime')) {
                return
            }
            form.find('.apply').click();
        }
    });
    editor.addButton('cancel', {
        title : 'Cancel and discard changes',

        text: 'Cancel',
        onclick: function() {
            if (form.data('ajaxTime')) {
                return
            }
            form.find('.cancel').click();
        }
    });
    editor.addShortcut('crtl+alt+s','save',
        function() {
            if (form.data('ajaxTime')) {
                return
            }
            form.find('.apply').click();
        });
}
