FEATURE_ENPOINT = "/api/features";
QA_FEATURE              = 2;
SCORE_FEATURE           = 3;
RUDE_WORD_FEATURE       = 4;
SEND_TO_SEARCH_FEATURE  = 5;

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
    loadHelper(FEATURE_ENPOINT + "?x=" + SCORE_FEATURE.toString(),
        function(data){
            drawFeature(
                "score-feuture",
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
        }
    )

    loadHelper(FEATURE_ENPOINT + "?x=" + RUDE_WORD_FEATURE.toString(),
        function(data){
            drawFeature(
                "rude_words-feuture",
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
        }
    )
    loadHelper(FEATURE_ENPOINT + "?x=" + SEND_TO_SEARCH_FEATURE.toString(),
        function(data){
            drawFeature(
                "link-to-se-feuture",
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
        }
    )
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