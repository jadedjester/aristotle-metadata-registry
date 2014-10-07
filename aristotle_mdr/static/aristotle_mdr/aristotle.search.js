$( document ).ready( function() {
    $('.dropdown-menu-form .dropdown-menu').on('click', function(e) {
        e.stopPropagation();
    });
});