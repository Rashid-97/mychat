function VebSoket(room_id, chat_type='chat') {

    var ws = null;
    if (location.protocol == 'https:') {
        ws = 'wss';
    }
    else if (location.protocol == 'http:') {
        ws = 'ws';
    }
    var socket = new WebSocket(ws+'://' + window.location.host + '/ws/'+chat_type+'/'+room_id);
    // var socket = new WebSocket('ws://127.0.0.1:6379/ws/chat');

    socket.onclose = function(){
        socket = new WebSocket(ws+'://' + window.location.host + '/ws/'+chat_type+'/'+room_id);
    }

    socket.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var check_mark = '';
        if (data.type == "typing" ) {
            $(".friend_name[id="+data.from_user+"]").find(".is_typing").text('..typing');
            if (data.from_user != my_id) {
                $(".message_konteyner").find(".is_typing").text('..typing');
            }
            setTimeout(function(){
                $('.is_typing').text('');
            }, 1000);
        }
        else if (data.type == "msg"){
            if ( $(".friend_name[id="+data.from_user+"]") != 'undefined' || $(".friend_name[id="+data.to_user+"]") != 'undefined') {

                if ( $(".friend_name[id="+data.from_user+"]").hasClass("mycustom_aktiv") || $(".friend_name[id="+data.to_user+"]").hasClass("mycustom_aktiv")) {

                    if (data.to_user != friend_id) {
                        start_or_end = 'justify-content-start'
                        msg_cotainer = 'msg_cotainer';
                        check_mark = '';
                    } else {
                        start_or_end = 'justify-content-end'
                        msg_cotainer = 'msg_cotainer_send';
                        check_mark = '<i id="check_mark_icon" class="fa fa-check" aria-hidden="true" is_read="false"></i>';
                    }
                    html_data = '<div class="d-flex ' + start_or_end + ' mb-4">' +
                        '                        <div class="img_cont_msg">' +
                        '                            <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg"' +
                        '                                 class="rounded-circle user_img_msg">' +
                        '                        </div>' +
                        '                        <div class="' + msg_cotainer + '">' +
                        data.message + check_mark +
                        '                           <span class="msg_time">2021.01.01</span>' +
                        '                        </div>' +
                        '                    </div>';
                    $("#msg_content").append(html_data);
                    $("#msg_text").val('');

                    if (data.to_user == my_id) {
                        socket.send(JSON.stringify(
                            {
                                'type': 'is_msg_readed',
                                'msg_from_user_id': friend_id
                            }
                        ));
                    }
                }
                else {
                    if ( $(".friend_name[id="+data.from_user+"]") != 'undefined' ) {
                        var msg_count = $(".friend_name[id="+data.from_user+"]").find(".not_readed_msgs").text();
                        if (msg_count == '') {
                            msg_count = 1;
                        }
                        else {
                            msg_count++;
                        }
                        $(".friend_name[id="+data.from_user+"]").find(".not_readed_msgs").text(msg_count);
                    }
                }

            }
        }
        else if (data.type == "user_logged_in_out"){
            if (data.logged_type == 1) {
                $(".friend_name[id="+data.logged_user_id+"]").find(".img_cont").find(".my_custom_on_off_icon_class").removeClass("offline");
            }
            else {
                $(".friend_name[id="+data.logged_user_id+"]").find(".img_cont").find(".my_custom_on_off_icon_class").addClass("offline");
            }
        }
        else if (data.type == 'msg_readed'){
            $("#msg_content").find("#check_mark_icon[is_read='false']").css('color', 'deepskyblue');
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