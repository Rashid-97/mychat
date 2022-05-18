function FriendRequestSocket(room_id='request_room') {

    var ws = null;
    if (location.protocol == 'https:') {
        ws = 'wss';
    }
    else if (location.protocol == 'http:') {
        ws = 'ws';
    }
    var socket = new WebSocket(ws+'://' + window.location.host + '/ws/request_friend/'+room_id);

    socket.onclose = function(){
        socket = new WebSocket(ws+'://' + window.location.host + '/ws/request_friend/'+room_id);
    }

    socket.onmessage = function (event) {
        console.log(event);
        var data = JSON.parse(event.data);

        if (data != '') {
            if (data.type == 'friend_request') {
                var status = null;
                if (data.to_user_id == my_id) {
                    $("#notification_div").parent().load(location.href + " #notification_div");
                    Swal.fire({
                        width: 300,
                        height: 200,
                        title: 'You got a friend request from '+ data.from_user_name,
                        showConfirmButton: true,
                        showDenyButton: true,
                        confirmButtonText: 'Add to friend',
                        denyButtonText: 'Decline',
                        showCloseButton: true,
                    }).then((result) => {
                      if (result.isConfirmed) {
                        status = true;
                      } else if (result.isDenied) {
                        status = false;
                      } else {
                          return false;
                      }
                      socket.send(JSON.stringify({
                        'type': 'friend_request_reaction',
                        'status': status,
                        'request_from_user_id': data.from_user_id,
                      }));
                    })
                }
            }
            else if (data.type == 'friend_request_reaction') {
                if (data.request_from_user_id == my_id) { // if I sent a friend request and getting response about user action (accepted or declined)
                    var icon_name = data.status ? 'success':'error';
                    Swal.fire({
                        icon: icon_name,
                        text: data.request_swal_msg
                    });
                }
                if (data.response_from_user_id == my_id) { // if I got a friend request and response to it
                    Swal.fire({
                       icon: 'info',
                       text: data.response_swal_msg
                    });
                    $("#notification_div").parent().load(location.href + " #notification_div");
                }
                if (data.status) { // if request was accepted
                    $("#private_chat_categ").load(location.href + " #private_chat_categ");
                    /* if new friend create new websocket */
                    var checkExist = setInterval(function() {
                        var new_user_room_id = $(".friend_name[id="+data.request_from_user_id+"]").attr('room_id');
                       if (new_user_room_id != 'undefined') {
                          roomID_arr[new_user_room_id] = new VebSoket(room_id);
                          clearInterval(checkExist);
                       }
                    }, 100);
                }
            }
        }
    }

    this.send = function (data) {
        return socket.send(JSON.stringify(data))
    }
    this.close = function(){
        return socket.close();
    }

    this.get_socket = function(){
        return socket;
    }
}