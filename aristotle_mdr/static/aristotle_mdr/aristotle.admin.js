// Scrap modals if they lose focus so they can be loaded with new content

$( document ).ready( function() {
    $('div.suggest_name_wrapper button').click(function(e) {
        var fields = $(this).data('suggestFields').split(',');
        var sep = $(this).data('separator');
        if (!sep) {
            sep = "-"
        }
        var name = "";
        $.each(fields, function(i,field) {
            input = $('#id_'+field);
            var field_name=input.val();
            if (input.parent().hasClass('autocomplete-light-widget')) {
                field_name=input.parent().find('.title').data('name');
                if (field_name){
                    field_name = field_name.trim();
                }
            }

            if (i==0) {
                name = field_name
            } else {
                name = name + sep + field_name;
            }
        })
        $(this).siblings('input').val(name);
        return false;
    });
});