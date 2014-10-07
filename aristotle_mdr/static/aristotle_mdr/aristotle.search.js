$( document ).ready( function() {
    $('.dropdown-menu-form .dropdown-menu').on('click', function(e) {
        e.stopPropagation();
        x = $(this).find("input:checked").length;
        if (x > 0) {
            $(this).parent().find(".badge").text(x);
        } else {
            $(this).parent().find(".badge").text('');   
        }
    });
    
    $("#search-input").keydown(function(e){
        if(e.which == 13) { // enter
            setTimeout(function(){
                $(".search-option:first").focus();
            },100);
        }
    });
    
    $(".dropdown-menu-form").keydown(function(e){
        if(e.keyCode == 40) { // down
            $(this).find("a").click();
            $(this).find("label").first().focus();
            return false; // stops the page from scrolling
        }
     });
     
    $(".dropdown-menu-form .dropdown-menu li").keydown(function(e){
        if(e.keyCode == 40) { // down
            $(this).next().find("label").focus();
            return false; // stops the page from scrolling
        }
        if(e.keyCode == 38) { // up
            $(this).prev().find("label").focus();
            return false; // stops the page from scrolling
        }
        if(e.keyCode == 13) { // enter
            $(this).find("label").click();
            return false; // stops the page from scrolling
        }
    });

    $('.dropdown-menu-form .dropdown-menu').each( function() {
        x = $(this).find("input:checked").length;
        if (x > 0) {
            $(this).parent().find(".badge").text(x);
        }
    });
    
    $('.dropdown-menu-date .dropdown-menu').on('click', function(e) {
        e.stopPropagation();
        x = $(this).find("input:checked").length;
        if (x > 0) {
            $(this).parent().find(".badge").text(x);
        } else {
            $(this).parent().find(".badge").text('');   
        }
    });

});