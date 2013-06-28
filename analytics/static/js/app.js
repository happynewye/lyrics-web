var options = {
        chart: {
            renderTo: 'chart',
            type: 'line'
        },
        yAxis: {
            title: {
                text: 'number of occurences'
            }
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                month: '%e. %b',
            }
        },
        plotOptions: {
            series: {
                }
        }
}

var map_series = function(data){
    var series = {
        name: data['name'],
        data: [],
    }

    var buckets = data['buckets']

    for (var point_key in buckets){
        var milis = buckets[point_key]['milis'];
        var count = buckets[point_key]['count'];
        series.data.push(
                [milis, count]
                )
    }
    console.log(series);
    return series
}

var show_source = function(name){
    console.log('showing source:',  name );
    $.getJSON('/api/data', {name: name}, function(data){
        options.series = []
        for (var series_key in data){
            options.series.push( map_series(data[series_key]))
        };
        var chart = new Highcharts.Chart(options);
    });
};

var list_sources = function(){
    console.log('listing sources');

    $.getJSON('/api/sources', function(data){
        $.Mustache.load('./static/templates.html')
            .done(function () {
                $('body').mustache('list_sources', data);
                // Register click listener.
                $('.source').click(function(event){
                    name = event.target.attributes.name.value
                    show_source(name);
                });
        });
    });
}

$(document).ready(function(){
    console.log('starting app');
    // Initial UI state.
    list_sources();
})
