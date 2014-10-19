 $(document).bind('hilightChoice', function(e, choice, autocomplete) {
    offset = $(choice).offset().top-$(choice).parent().offset().top
    $(choice).parent().scrollTop(offset);
});
