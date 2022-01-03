$(document).ready(function(){
    console.log("Document ready");
    //connect to the socket server.

{% for bot in bots %}
    var socket_{{ bot.name }} = io.connect('http://' + document.domain + ':' + location.port + '/logs/{{ bot.name }}');
    var data_received_{{ bot.name }} = $('#log_{{ bot.name }}').html().split("\n");
    //receive details from server
    socket_{{ bot.name }}.on('data', function(msg) {
        console.log("Received log -> " + msg.data);
        //maintain a list of log data
        if (data_received_{{ bot.name }}.length >= 20){
            data_received_{{ bot.name }}.shift()
        }
        data_received_{{ bot.name }}.push(msg.data);
        log_string = '';
        for (var i = 0; i < data_received_{{ bot.name }}.length; i++){
            log_string = log_string + data_received_{{ bot.name }}[i].toString() + '\n';
        }
        $('#log_{{ bot.name }}').html(log_string);
    });
{% endfor %}
    
    var socket_main = io.connect('http://' + document.domain + ':' + location.port + '/log');
    var data_received_main = $('#main_log').html().split("\n");
    //receive details from server
    socket_main.on('data', function(msg) {
        console.log("Received log -> " + msg.data);
        //maintain a list of log data
        if (data_received_main.length >= 20){
            data_received_main.shift()
        }
        data_received_main.push(msg.data);
        log_string = '';
        for (var i = 0; i < data_received_main.length; i++){
            log_string = log_string + data_received_main[i].toString() + '\n';
        }
        $('#main_log').html(log_string);
    });
});