FEATURE_ENPOINT = "/api/features";
SCORE_FEATURE

$(document).ready(function() {
    loadHelper(FEATURE_ENPOINT + "?x=3&y=4",
        function(data){
            drawFeature(
                "manual-feutures",
                "Рейтинг сообщения к количеству грубых слов в комментарии",
                data.x_name,
                data.y_name,
                data.positive,
                data.negative,
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