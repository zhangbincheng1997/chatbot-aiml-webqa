function chat(message) {
    $.ajax({
        url: "chat",
        type: "GET",
        data: {"message": message},
        success: function (data) {
            var ans = '<div class="answer">'
                + '<div class="icon left"><img src="images/ai.png"/></div>'
                + '<div class="answer_text"><p style="white-space: pre-line;">' + data + '</p><i></i>'
                + '</div></div>';

            $('.speak_box').append(ans);
            fit_screen();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert("服务器出错：" + XMLHttpRequest.status);
        }
    });
}

function key_up() {
    var text = $('.chat_box input').val();
    if (text == '') {
        $('.write_list').remove();
    } else {
        var str = '<div class="write_list">' + text + '</div>';
        $('.footer').append(str);
        $('.write_list').css('bottom', $('.footer').outerHeight());
    }
}

function send_message() {
    $('.write_list').remove();
    var text = $('.chat_box input').val();
    if (text == '') {
        alert('请输入聊天内容！');
        $('.chat_box input').focus();
        $('body').css('background-image', 'url(/images/bg.jpg)');
    } else {
        var str = '<div class="question">'
            + '<div class="icon right"><img src="images/me.png"/></div>'
            + '<div class="question_text clear"><p style="white-space: pre-line;">' + text + '</p><i></i>'
            + '</div></div>';

        $('.speak_box').append(str);
        $('.chat_box input').val('');
        $('.chat_box input').focus();

        fit_screen();
        auto_width();
        chat(text);
    }
}

function fit_screen() {
    $('.speak_box, .speak_window').animate({scrollTop: $('.speak_box').height()}, 500);
}

function auto_width() {
    $('.question_text').css('max-width', $('.question').width() - 60);
}