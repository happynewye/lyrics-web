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
}

var show_module = function(_id){
    console.log('showing module', _id);

    $.getJSON('/api/data', {_id: _id}, function(data){
        options.series = []
        for (var key in data){
            options.series.push({
                'name': key,
                'data': data[key]
            });
        }
        var chart = new Highcharts.Chart(options);
    });
};

var show_modules = function(){
    console.log('listing modules');

    $.getJSON('/api/list_modules', function(data){
        $.Mustache.load('./static/templates.html')
            .done(function () {
                $('body').mustache('list_modules', data);
                // Register click listener.
                $('.module_option').click(function(event){
                    _id = event.target.attributes.module_id.value;
                    show_module(_id);
                });
        });
    });
}

$(document).ready(function(){
    console.log('starting app');
    // Initial UI state.
    show_modules();
})
