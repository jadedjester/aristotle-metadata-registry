// Scrap modals if they lose focus so they can be loaded with new content
$(document).on('hidden.bs.modal', function (e) {
    $(e.target).removeData('bs.modal');
});

var glossaryList = [];
var glossaryLookup = {}

function getGlossaryList() {
    $.ajax({
        url: '/glossary/ajaxlist',
        dataType : 'json',
    }).done(function(data) {
        glossaryList=[]
        for (var i = 0; i < data.length; i++) {
            i=data[i];
            console.log(i);
            glossaryLookup[i.id] = i;
            glossaryList.push({text:i.name,value:i.id});
        }
    })
    return glossaryList;
}
