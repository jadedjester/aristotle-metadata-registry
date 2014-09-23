/* This block is derived from django-inplaceedit with minor tweaks */

(function($){
    $(document).ready(function () {
        var options = {"getFieldUrl": "/inplaceeditform/get_field/",
                       "saveURL": "/inplaceeditform/save/",
                       "successText": "Successfully saved",
                       "eventInplaceEdit": "dblclick",
                       "disableClick": true,
                       "autoSave": false,
                       "unsavedChanges": "You have unsaved changes",
                       "enableClass": "enable",
                       "fieldTypes": "input, select, textarea",
                       "focusWhenEditing": true};
        var inplaceManager = $(".inplaceedit").inplaceeditform(options);

            if ($(".inplaceedit").size()) {

var enabledEditText = "<i class='fa fa-edit'></i> Edit";
var disabledEditText = "<i class='fa fa-power-off'></i> Editing...";
var toggleInplaceEdit = function () {
    var trigger = $(this);
    if (trigger.hasClass('active')) {
        inplaceManager.disable();
        trigger.removeClass('active');
        trigger.html(enabledEditText);
        $('.inline_action').removeClass('enable');
        trigger.parent().removeClass('active');
        $('#progress.alert').slideToggle()
        $('#progress.alert').addClass('alert-success').removeClass('alert-warning');
    } else {
        inplaceManager.enable();
        trigger.addClass('active');
        trigger.html(disabledEditText);
        $('.inline_action').addClass('enable');
        trigger.parent().addClass('active');
        $('#progress.alert').removeClass('hidden').hide()
        $('#progress.alert').addClass('alert-danger').removeClass('alert-success');
        $('#progress.alert').slideToggle();
    }
};

var toolbar = $("#ActivateInplaceEdit");
var actions = toolbar.find(".toolbarActions");
toolbar.replaceWith("<a class='toolbarAction btn btn-default' href='#' id=\"ActivateInplaceEdit\" accesskey='e'>" + enabledEditText + "</a>");
$("#ActivateInplaceEdit").click(toggleInplaceEdit);
                    }
        });
    })(jQuery);