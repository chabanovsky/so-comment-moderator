var verifyClass = ".verify";

$(document).ready(function() {

    $(verifyClass).click(function(event){
        event.preventDefault();
        href = event.target.href;

        loadHelper(href, function(data){
            window.location.reload();
        }, function(){
            alert("Cannot send verify request.");
        })

        return false;
    });
    
})