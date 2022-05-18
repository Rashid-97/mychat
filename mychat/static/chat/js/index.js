$('.action_menu_btn').click(function () {
    $('.action_menu').toggle();
});

$(document).on('click','#dropdownFRMenuLink', function (event) {
    $('#notification_dropdown_menu').toggle();
});

function scroll_to_bottom(id) {
    var objDiv = document.getElementById(id);
    objDiv.scrollTop = objDiv.scrollHeight;
}

function get_time(time = '') {
    if (time != '') {
        var date = new Date(time);
    } else {
        var date = new Date();
    }
    return date.getHours() + ':' + date.getMinutes();
}
