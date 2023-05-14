// import dayjs from 'dayjs';

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


// タスク完了ボタンを押したとき
$('.task-complete').on('submit', function(e) {
    e.preventDefault();

    // 受け取った .task-complete 要素に対して、その .task-complete__btn の値を取得する
    var task_pk = $(this).find('.task-complete__btn').val();

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
        console.log("length" + $('#my-tasks tr').length);
        $(`#task-${task_pk}`).remove();
        if ($('#task-table tr').length == 1) {
            $('#task-set').html("<p id='task-notset'>タスクはまだ設定されていません</p>");
        }
    });
});

// タスク編集完了時
$('.task-edit__form').on('submit', function(e) {
    e.preventDefault();

    var task_pk = $(this).find('.task-edit__submit-btn').val();
    console.log("task_pk " + task_pk);

    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {
            'name': 'task-edit',
            'task-pk': task_pk,
            'title': $(this).find('input[name="title"]').val(),
            'content': $(this).find('input[name="content"]').val(),
            'deadline_0': $(this).find('input[name="deadline_0"]').val(),
            'deadline_1': $(this).find('input[name="deadline_1"]').val(),
        },
        'dataType': 'json'
    })
    .done(function(response){
        console.log(response);
        var task_pk = response['task-pk'];
        var task_title = response['title'];
        var task_content = response['content'];
        var has_deadline = response["has_deadline"];
        var deadline_passed = response["deadline_passed"];
        var deadline = response["deadline"];
        var remaining_datetime = response["remaining_datetime"];
    
        // HTMLを書き換える
        var task_row = $('#task-' + task_pk);
        task_row.find('.task-title').text(task_title);
        task_row.find('.task-content').text(task_content);
        if (has_deadline) {
            task_row.find('.task-deadline').text(deadline);
            console.log(deadline_passed);
            if (deadline_passed) {
                console.log("deadline passed!");
                task_row.find('.task-remaining-datetime').html(`<b>${remaining_datetime}</b>過ぎています`);
            } else {
                task_row.find('.task-remaining-datetime').text(`締切まで: ${remaining_datetime}`);
            }
        } else {
            task_row.find('.task-no-deadline').text('締切なし');
        }
    });
    
    function secondsToTime(seconds) {
        console.log("seconds" + seconds);
        var hour = Math.floor(seconds / 3600);
        var minute = Math.floor((seconds - hour * 3600) / 60);
        var second = Math.floor(seconds - hour * 3600 - minute * 60);
        return hour + '時間' + minute + '分' + second + '秒';
    }    
});