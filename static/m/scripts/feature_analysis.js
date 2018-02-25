var FEATURE_ENPOINT = "/api/features";
var QA_FEATURE              = 0;
var SCORE_FEATURE           = 1;
var RUDE_WORD_FEATURE       = 2;
var SEND_TO_SEARCH_FEATURE  = 3;
var WIKTIONARY_ORG_OBSCENE_WORD_FEATURE = 4;
var WIKTIONARY_ORG_ABUSIVE_WORD_FEATURE = 5;
var WIKTIONARY_ORG_RUDE_WORD_FEATURE    = 6;
var WIKTIONARY_ORG_IRONY_WORD_FEATURE   = 7;
var WIKTIONARY_ORG_CONTEMPT_WORD_FEATURE= 8;
var WIKTIONARY_ORG_NEGLECT_WORD_FEATURE = 9;
var WIKTIONARY_ORG_HUMILIATION_WORD_FEATURE = 10;

var waitingDiv = '<div class="wait">Информация загружается...</div>';
var scoreContainerId = "score-feature";
var rudeWordContainerId = "rude-words-feature";
var linkToSEContainerId = "link-to-se-feature";
var obsceneWordContainerId = "obscene-word-feature";
var abusiveWordContainerId = "abusive-word-feature";
var rudeWordWikiContainerId = "rude-word-wiki-feature";
var ironyWordContainerId = "irony-word-feature";
var contemptWordContainerId = "contempt-word-feature";
var negletWordContainerId = "neglet-word-feature";
var humiliationWordContainerId = "humiliation-word-feature";

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

function addFeature(containerId, feature, title) {
    $("#" + containerId + " a").click(function(event){
        event.preventDefault();
        var old_value = $("#" + containerId).html()
        $("#" + containerId).html(waitingDiv)

        loadHelper(FEATURE_ENPOINT + "?x=" + feature.toString(),
            function(data){
                $("#" + containerId).css("height", "400px");
                drawFeature(
                    containerId,
                    title,
                    data.x_name,
                    "Количество",
                    group_by_count(data.positive),
                    group_by_count(data.negative),
                    "Оскорбление",
                    "Обычный комментарий" 
                )
            },
            function(){
                alert("Could not load feature data for the feature #" + feature.toString())
                $("#" + containerId).html(old_value)
            }
        )
    });
}

$(document).ready(function() {
    addFeature(scoreContainerId, SCORE_FEATURE, "Рейтинг сообщения");
    addFeature(rudeWordContainerId, RUDE_WORD_FEATURE, "Кол-во грубых слов");
    addFeature(linkToSEContainerId, SEND_TO_SEARCH_FEATURE, "Отправка в поиск")
    addFeature(obsceneWordContainerId, WIKTIONARY_ORG_OBSCENE_WORD_FEATURE, "Кол-во матерных слов");
    addFeature(abusiveWordContainerId, WIKTIONARY_ORG_ABUSIVE_WORD_FEATURE, "Кол-во бранных слов");
    addFeature(rudeWordWikiContainerId, WIKTIONARY_ORG_RUDE_WORD_FEATURE, "Кол-во грубых слов (Вики)");
    addFeature(ironyWordContainerId, WIKTIONARY_ORG_IRONY_WORD_FEATURE, "Кол-во слов иронии");
    addFeature(contemptWordContainerId, WIKTIONARY_ORG_CONTEMPT_WORD_FEATURE, "Кол-во слов призрения");
    addFeature(negletWordContainerId, WIKTIONARY_ORG_NEGLECT_WORD_FEATURE, "Кол-во слов пренебрежения");
    addFeature(humiliationWordContainerId, WIKTIONARY_ORG_HUMILIATION_WORD_FEATURE, "Кол-во слов унижения");
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