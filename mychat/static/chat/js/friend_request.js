var friend_request_socket = new FriendRequestSocket();

$(document).on("click", "#add_to_friend", function (){
    var to_user_id = $(this).attr("user_id");

    friend_request_socket.send({
        'type': 'friend_request',
        'from_user_id': my_id,
        'to_user_id': to_user_id
    });

    $(this).attr('disabled', 'disabled');

});
$(document).on("click", ".notification_reply_btn", function(){
    var status = $(this).attr('id');
    status = status == 1? true : false;
    var request_from_user_id = $('#request_from_user_id').attr('val');
    friend_request_socket.send({
        'type': 'friend_request_reaction',
        'status': status,
        'request_from_user_id': request_from_user_id,
    });

});