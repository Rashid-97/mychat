function QrupVebSoket(room_id) {

    var ws = null;
    if (location.protocol == 'https:') {
        ws = 'wss';
    }
    else if (location.protocol == 'http:') {
        ws = 'ws';
    }
    var socket = new WebSocket(ws+'://' + window.location.host + '/ws/group_chat/'+room_id);
    // var socket = new WebSocket('ws://127.0.0.1:6379/ws/chat');

    socket.onclose = function(){
        socket = new WebSocket(ws+'://' + window.location.host + '/ws/group_chat/'+room_id);
    }

    socket.onmessage = function (event) {
        var data = JSON.parse(event.data);

        if (data.type == 'group_msg') {
            var html_data = '';
            var start_or_end = '';
            var msg_cotainer = '';
            if (data.from_user != my_id) {
                start_or_end = 'justify-content-start'
                msg_cotainer = 'msg_cotainer';
            } else {
                start_or_end = 'justify-content-end'
                msg_cotainer = 'msg_cotainer_send';
            }
            html_data += '<div class="d-flex ' + start_or_end + ' mb-4">' +
            '                        <div class="img_cont_msg">' +
            '                        </div>' +
            '                        <div class="' + msg_cotainer + '">' +
                                        data.msg+
            '                           <span class="msg_time">' + get_time(data.sent_date) + '</span>' +
            '                        </div>' +
            '                    </div>';
            $("#group_msg_content").append(html_data);
            $("#group_msg_text").val('');
            scroll_to_bottom("group_msg_content");
        }
        else if (data.type == 'group_typing') {
            console.log(data.group_id)
            if (data.from_user_id != my_id) {
                $(".group_name[id="+data.group_id+"]").find('.group_is_typing').text(data.from_user+ ' is typing..');
                $("#group_chat_container").find('.group_is_typing').text(data.from_user+ ' is typing..');
            }

            setTimeout(function(){
                $('.group_is_typing').text('');
            }, 1000);
        }
    }

    this.send = function (data){
        return socket.send(JSON.stringify(data));
    }
    this.close = function(){
        return socket.close();
    }

    this.get_socket = function(){
        return socket;
    }

}