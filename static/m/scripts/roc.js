ROC_SERVER_ENDPOINT = "/api/roc/";
var rocRootContainerId = "roc-chart-root";
var rocContainerId = "roc-chart";

function generateContainer(index) {
    return '<p><div id="roc-chart' + index.toString() + '" style="height:500px; width: 100%;"></div></p>';
}
$(document).ready(function(){
    var page = $("#roc-id").text()
    var url = ROC_SERVER_ENDPOINT + "?page=" + page
    loadHelper(url, function(data){
        toDraw = []
        
        for (var index = 0; index < data.items.length; index++) {
            item = data.items[index];
            extra = JSON.parse(item.extra);
            tp = extra.rude_right / extra.rude_total;
            fp = (extra.normal_total-extra.normal_right) / extra.normal_total;
            points = [];
            points.push({ x: 0, y: 0 });
            points.push({
                y: tp,
                x: fp,
                label: new Date(item.added), 
                indexLabel: "точность: " + Math.round(extra.acc * 100) / 100 
            });
            points.push({ x: 1, y: 1 });

            toDraw.push({id: rocContainerId + index.toString(), points: points, added: item.added});
            $("#" + rocRootContainerId).append(generateContainer(index))
        }
        for(var index = 0; index < toDraw.length; index++){
            var item = toDraw[index];
            drawROC(item.id, item.points, item.added);
        }
    }, function(){

    });
})

function drawROC(container, points, date) {
    dateParts = (new Date(date)).toISOString().split('T')
    var chart = new CanvasJS.Chart(container, {
        animationEnabled: true,
        title: {
            text: "РХП от " + dateParts[1].split('.')[0] + " " + dateParts[0]
        },
        axisX: {
            title: "ложно отрицательные",
            minimum: 0,
            maximum: 1
        },
        axisY: {
            title: "истенно положительные",
            minimum: 0,
            maximum: 1
        },
        data: [{
            indexLabelFontColor: "darkSlateGray",
            name: "views",
            type: "area",
            yValueFormatString: "#,##0.0",
            xValueFormatString: "#,##0.0",
            dataPoints: points
        }]
    });
    chart.render();
    
}