ROC_SERVER_ENDPOINT = "/api/roc/";

$(document).ready(function(){
    loadHelper(ROC_SERVER_ENDPOINT, function(data){
        for (var index = 0; index < data.items.lenght; index++) {
            item = data.items[index];
        }
    }, function(){

    });
})