function updateCheckboxBadge(menu) {
    x = $(menu).find("input:checked").length;
    if (x > 0) {
        $(menu).parent().find(".badge").text(x);
    } else {
        $(menu).parent().find(".badge").text('');   
    }
}

function updateAdvancedDateDetails(menu) {
    x = $(menu).find("input:checked");
    if (x.length > 0 && x[0].value != 'a') {
        x=x[0];
        $(menu).parent().find(".details").text($("label[for='"+x.id+"']").text());
    } else {
        $(menu).parent().find(".details").text('');
    }
}

$( document ).ready( function() {
    $('.dropdown-menu-form .dropdown-menu').on('click', function(e) {
        e.stopPropagation();
        updateCheckboxBadge(this);
    });
    $('.dropdown-menu-form .dropdown-menu').each( function() {
        updateCheckboxBadge(this);
    });
    $('.dropdown-menu-date .dropdown-menu').on('click', function(e) {
        e.stopPropagation();
        updateAdvancedDateDetails(this);
    });
    $('.dropdown-menu-date .dropdown-menu').each( function() {
        updateAdvancedDateDetails(this);
    });
    
    $('.dropdown-menu-date .dropdown-menu .input-group.date').each( function() {
        console.log(this)
        $(this).on("dp.change", function() {
            // change(this);
            console.log(this)
            $(self).parents(".dropdown-menu").first().find("[value='X']").prop("checked", true);
        
    
        });
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



});