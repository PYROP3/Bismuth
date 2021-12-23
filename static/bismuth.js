$(document).ready(function(){
    console.log("Document ready");
    //connect to the socket server.
    var socket_xeroque = io.connect('http://' + document.domain + ':' + location.port + '/logs/xeroque');
    var data_received_xeroque = [];
    //receive details from server
    socket_xeroque.on('data', function(msg) {
        console.log("Received log -> " + msg.data);
        //maintain a list of log data
        if (data_received_xeroque.length >= 20){
            data_received_xeroque.shift()
        }
        data_received_xeroque.push(msg.data);
        log_string = '';
        for (var i = 0; i < data_received_xeroque.length; i++){
            log_string = log_string + data_received_xeroque[i].toString() + '\n';
        }
        $('#log_xeroque').html(log_string);
    });
    
    var socket_main = io.connect('http://' + document.domain + ':' + location.port + '/log');
    var data_received_main = [];
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
        $('#log_main').html(log_string);
    });
});