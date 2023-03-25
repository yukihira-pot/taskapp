function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.task-complete').on('submit', function(e) {
    e.preventDefault();

    var task_pk = $('.task-complete-btn').val()

    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {
            "name": "task-complete",
            'task-pk': task_pk,
        },
        'dataType': 'json'
    })
    .done(function(response){
        $(`#task-${task_pk}`).remove();
        if ($('#my-tasks ul').length == 0) {
            $('#task-set').html("<p id='task-notset'>タスクはまだ設定されていません</p>");
        }
    });
});