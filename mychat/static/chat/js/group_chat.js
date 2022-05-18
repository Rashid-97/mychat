var curr_group_id = null;
var get_group_msg_url = null;
var get_group_msg_sql_offset = 0;
var group_roomID_arr = {};

if ( $('.group_name').length <= 100 ) { // for more than 100 connections needs to be premium :)
    $('.group_name').each(function() {
        var room_id = $(this).attr("id");
        group_roomID_arr [room_id] = new QrupVebSoket(room_id);
    });
}
$(".group_name").click(function(){
    $("#friend_chat_container").css('display', 'none');
    $("#group_chat_container").css('display', 'flex');

    $(".chat_categ_li").removeClass('active mycustom_aktiv')
    $(this).addClass('active mycustom_aktiv')

    $("#group_msg_text").focus()
    var group_id = $(this).attr("id");
    curr_group_id = group_id;
    get_group_msg_url = $(this).attr("url")
    var group_name = $(this).find(".group_info").text();

    curr_room_id = group_id;
    get_group_msg_sql_offset = 0;

    $("#chat_with").text(group_name);

    $.ajax({
        url: get_group_msg_url,
        type: 'post',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'group_id': group_id,
            'sql_offset': get_group_msg_sql_offset,
        },
        success: function(resp){
            var msgs = resp.data;
            // var msgs = JSON.parse(resp.data);
            var html_data = get_group_msg(msgs);
            $("#group_msg_content").html(html_data);
            scroll_to_bottom("group_msg_content");
        },
        error: function (err){
            console.log(err);
        }
    });
});

function get_group_msg(msgs) {
    var html_data = '';
    var start_or_end = '';
    var msg_cotainer = '';
    for (var i = msgs.length - 1; i >= 0; i--) {
        var fields = msgs[i];
        var check_mark = '';

        if (fields.who_sent != my_id) {
            start_or_end = 'justify-content-start'
            msg_cotainer = 'msg_cotainer';
            // check_mark = '';
        } else {
            start_or_end = 'justify-content-end'
            msg_cotainer = 'msg_cotainer_send';
            // check_mark = '<i id="check_mark_icon" class="fa fa-check" aria-hidden="true" ' + is_read + '></i>';
        }

        html_data += '<div class="d-flex ' + start_or_end + ' mb-4">' +
            '                        <div class="img_cont_msg">' + fields.from_user +
            '                        </div>' +
            '                        <div class="' + msg_cotainer + '">' +
            fields.text + check_mark +
            '                           <span class="msg_time">' + get_time(fields.sent_date) + '</span>' +
            '                        </div>' +
            '                    </div>';
    }
    return html_data;
}

$("#group_msg_text").keyup(function (e) {
    var key_code = e.keyCode | e.which;

    if (key_code == 13) {

        $("#group_send_msg_btn").click();

    } else {
        if (curr_room_id != null) {
            group_roomID_arr[curr_room_id].send({
                'type': 'is_typing',
                'group_id': curr_group_id
            });
        }
    }

});


$("#group_send_msg_btn").click(function () {
    var msg_text = $("#group_msg_text").val();
    if (msg_text.trim() != '') {

        if (curr_room_id != null) {
            group_roomID_arr[curr_room_id].send({
                'type': 'is_msg',
                'group_id': curr_group_id,
                'from_user': my_id,
                'msg': msg_text
            });
        }

    }
});

$("#group_msg_content").on('scroll', function (e) {
    if ($(this).scrollTop() == 0) {
        get_group_msg_sql_offset += 10;
        $.ajax({
            url: get_group_msg_url,
            type: 'post',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'group_id': curr_group_id,
                'sql_offset': get_group_msg_sql_offset
            },
            success: function(resp){
                var msgs = resp.data;
                var html_data = get_group_msg(msgs);
                $("#group_msg_content").prepend(html_data);
            },
            error: function(err){
                console.log(err);
            }
        });
        $(this).scrollTop(1);
    }
});

/*
get data on scroll
        */