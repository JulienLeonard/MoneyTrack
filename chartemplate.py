charttemplate = """<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<script src="http://code.highcharts.com/highcharts.js"></script>
<div id="%CONTAINER%" style="height: 750px"></div>
<script>
$(function () {
    $('#%CONTAINER%').highcharts({
        title: {
            text: '%TITLE%',
            x: -20 //center
        },
        subtitle: {
            text: 'Source: moneytracker',
            x: -20
        },
        xAxis: {
            categories: [%CATEGORIES%]
        },
        yAxis: {
            title: {
                text: '%YAXIS%'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: 'C'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '%NAME%',
            data: [%DATA%]
        }]
    });
});
</script>"""
