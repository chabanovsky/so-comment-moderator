var FEATURE_ENPOINT = "/api/features";
var QA_FEATURE              = 2;
var SCORE_FEATURE           = 3;
var RUDE_WORD_FEATURE       = 4;
var SEND_TO_SEARCH_FEATURE  = 5;

var waitingDiv = '<div class="wait">Информация загружается...</div>';
var scoreContainerId = "score-feuture";
var rudeWordContainerId = "rude_words-feuture";
var linkToSEContainerId = "link-to-se-feuture";

function group_by_count(data){
    var dictionary = {};
    for (var index = 0; index < data.length; index++) {
        item = data[index]
        if (item.x in dictionary) {
            dictionary[item.x] += 1
        } else {
            dictionary[item.x] = 1
        }
    }
    new_data = []
    for(key in dictionary){
        var value = dictionary[key];
        new_data.push({
            "x": parseInt(key),
            "y": value
        })
    }
    return new_data
}

$(document).ready(function() {
    $("#" + scoreContainerId + " a").click(function(event){
        event.preventDefault();
        var old_value = $("#" + scoreContainerId).html()
        $("#" + scoreContainerId).html(waitingDiv)

        loadHelper(FEATURE_ENPOINT + "?x=" + SCORE_FEATURE.toString(),
            function(data){
                $("#" + scoreContainerId).css("height", "400px");
                drawFeature(
                    scoreContainerId,
                    "Рейтинг сообщения",
                    data.x_name,
                    "Количество",
                    group_by_count(data.positive),
                    group_by_count(data.negative),
                    "Оскорбление",
                    "Обычный комментарий" 
                )
            },
            function(){
                alert("Could not load feature data.")
                $("#" + scoreContainerId).html(old_value)
            }
        )
    });

    $("#" + rudeWordContainerId + " a").click(function(event){
        event.preventDefault();
        var old_value = $("#" + rudeWordContainerId).html()
        $("#" + rudeWordContainerId).html(waitingDiv)

        loadHelper(FEATURE_ENPOINT + "?x=" + RUDE_WORD_FEATURE.toString(),
            function(data){
                $("#" + rudeWordContainerId).css("height", "400px");
                drawFeature(
                    rudeWordContainerId,
                    "Кол-во грубых слов",
                    data.x_name,
                    "Количество",
                    group_by_count(data.positive),
                    group_by_count(data.negative),
                    "Оскорбление",
                    "Обычный комментарий" 
                )
            },
            function(){
                alert("Could not load feature data.")
                $("#" + rudeWordContainerId).html(old_value)
            }
        )
    });
    
    $("#" + linkToSEContainerId + " a").click(function(event){    
        event.preventDefault();
        var old_value = $("#" + linkToSEContainerId).html()
        $("#" + linkToSEContainerId).html(waitingDiv)

        loadHelper(FEATURE_ENPOINT + "?x=" + SEND_TO_SEARCH_FEATURE.toString(),
            function(data){
                $("#" + linkToSEContainerId).css("height", "400px");
                drawFeature(
                    linkToSEContainerId,
                    "Отправка в поиск",
                    data.x_name,
                    "Количество",
                    group_by_count(data.positive),
                    group_by_count(data.negative),
                    "Оскорбление",
                    "Обычный комментарий" 
                )
            },
            function(){
                alert("Could not load feature data.")
                $("#" + linkToSEContainerId).html(old_value)
            }
        )
    });
});

function drawFeature(container, title, x_name, y_name, positive_class_data, negative_class_data, positive_class_name, negative_class_name){
    $("#" + container).empty()
    var chart = new CanvasJS.Chart(container, {
        animationEnabled: true,
        title:{
            text: title
        },
        axisX: {
            title: x_name
        },
        axisY:{
            title: y_name
        },
        data: [{
            type: "scatter",
            toolTipContent: "<span style=\"color:#4F81BC \"><b>{name}</b></span><br/><b> " + x_name + ":</b> {x} <br/><b> " + y_name + ":</b></span> {y} ",
            name: positive_class_name,
            showInLegend: true,
            dataPoints: positive_class_data
        },
        {
            type: "scatter",
            name: negative_class_name,
            showInLegend: true, 
            toolTipContent: "<span style=\"color:#C0504E \"><b>{name}</b></span><br/><b> " + x_name + ":</b> {x} <br/><b> " + y_name + ":</b></span> {y} ",
            dataPoints: negative_class_data
        }]
    });
    chart.render();
}