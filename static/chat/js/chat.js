var csrftoken = $(".contacts input[name='csrfmiddlewaretoken']").val();
var friend_id = null;
var mysocket = null;
var get_msg_url = null;
var get_msg_sql_offset = 0;

var roomID_arr = {};
var curr_room_id = null;
$('.friend_name').each(function() {
    var room_id = $(this).attr("room_id");
    roomID_arr[room_id] = new VebSoket(room_id);
    roomID_arr[room_id].get_socket().onopen = function (event){
        this.send(JSON.stringify( {
            'type': 'is_user_logged_in_out',
            'logged_type': 1 // logged in = 1, logged out = 0
        } )); // for user online/offline status
    }
});

$(document).on('click','.friend_name_action', function () {
    $("#group_chat_container").css('display', 'none');
    $("#friend_chat_container").css('display', 'flex');
    $("#msg_text").focus()
    $(".chat_categ_li").removeClass('active mycustom_aktiv')
    $(this).addClass('active mycustom_aktiv')
    $(this).find(".not_readed_msgs").text(""); // clear not readed msg count
    var friend_name = $(this).attr("friend_name");
    $("#chat_with").text(friend_name);

    curr_room_id = $(this).attr("room_id");
    friend_id = $(this).attr('id')
    get_msg_url = $(this).attr('url')
    get_msg_sql_offset = 0;

    $.ajax({
        url: get_msg_url,
        type: 'post',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'friend_id': friend_id,
            'sql_offset': get_msg_sql_offset
        },
        success: function (resp) {
            var msgs = JSON.parse(resp.msgs)
            var html_data = get_msg(msgs);
            $("#msg_content").html(html_data);
            scroll_to_bottom("msg_content");

            if ( $(".friend_name[id="+friend_id+"]").find(".not_readed_msgs").text != '' ) {
                // after user see the message websocket will get data to change checkmark as checked for friend
                roomID_arr[curr_room_id].send({
                    'type': 'is_msg_readed',
                    'msg_from_user_id': friend_id
                });
            }
        },
        error: function (err) {
            console.log(err);
        }
    });

});

$("#msg_text").keyup(function (e) {
    var key_code = e.keyCode | e.which;

    if (key_code == 13) {

        $("#send_msg_btn").click();

    } else {
        if (curr_room_id != null) {
            roomID_arr[curr_room_id].send({
                'type': 'is_typing'
            });
        }
    }

});


$("#send_msg_btn").click(function () {
    var msg_text = $("#msg_text");
    if (msg_text.val().trim() != '') {

        if (curr_room_id != null) {
            roomID_arr[curr_room_id].send({
                'type': 'is_msg',
                'to_user': friend_id,
                'msg': msg_text.val()
            });
        }

    }
});


$("#msg_content").on('scroll', function (e) {
    if ($(this).scrollTop() == 0) {
        get_msg_sql_offset += 10;
        $.ajax({
            url: get_msg_url,
            type: 'post',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'friend_id': friend_id,
                'sql_offset': get_msg_sql_offset
            },
            success: function(resp){
                var msgs = JSON.parse(resp.msgs)
                var html_data = get_msg(msgs);
                $("#msg_content").prepend(html_data);
            },
            error: function(err){
                console.log(err);
            }
        });
        $(this).scrollTop(1);
    }
});

$("#block_friend").click(function(){
    var url = $(this).attr("url");
    $.ajax({
        url: url,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrftoken,
            "friend_id": friend_id
        },
        success: function(resp){
            if (resp.success) {
                Swal.fire("Friend has been blocked!");
            }
        },
        error: function(err){
            console.log(err);
        }
    });
});

$(document).on('click', '#search_people', function(event){
    event.preventDefault();
    $("#search_people_container").html('');
    var search_people_url = $(this).attr("search_people_url");
    $.ajax({
        url: search_people_url,
        type: 'post',
        data: {
            "csrfmiddlewaretoken": csrftoken,
        },
        success: function (resp){
            var html_data = "";
            for (var i in resp){
                var is_offline = !resp[i].is_online ? 'offline':'';
                var online_icon = '<span class="my_custom_on_off_icon_class online_icon '+is_offline+'"></span>';
                html_data += "<div class='row'>";
                html_data += "<div class='col-md-4'>"+online_icon+"</div>";
                html_data += "<div class='col-md-4'>"+resp[i].username+"</div>";
                html_data += "<div class='col-md-4'><button class='btn btn-primary' id='add_to_friend' user_id='"+resp[i].person_id+"'>Add to friend</button></div>";
                html_data += "</div>";
            }
            $("#search_people_container").prepend(html_data);
            // $(html_data).appendTo('body').modal();

        },
        error: function (err){
            console.log(err);
        }
    });
});
$("#dropdownFRMenuLink").click(function(){
    $(this).parent().find( '.dropdown-menu').toggle();
});

function get_msg(msgs) {
    var html_data = '';
    var start_or_end = '';
    var msg_cotainer = '';
    for (var i = msgs.length - 1; i >= 0; i--) {
        var fields = msgs[i].fields;
        var check_mark = '';

        if (fields.from_user == friend_id) {
            start_or_end = 'justify-content-start'
            msg_cotainer = 'msg_cotainer';
            check_mark = '';
        } else {
            start_or_end = 'justify-content-end'
            msg_cotainer = 'msg_cotainer_send';
            var is_read = (fields.is_read) ? 'is_read="true" style="color:deepskyblue;"' : 'is_read="false"';
            check_mark = '<i id="check_mark_icon" class="fa fa-check" aria-hidden="true" ' + is_read + '></i>';
        }


        html_data += '<div class="d-flex ' + start_or_end + ' mb-4">' +
            '                        <div class="img_cont_msg">' +
            '                        </div>' +
            '                        <div class="' + msg_cotainer + '">' +
            fields.text + check_mark +
            '                           <span class="msg_time">' + get_time(fields.sent_date) + '</span>' +
            '                        </div>' +
            '                    </div>';
    }
    return html_data;
}