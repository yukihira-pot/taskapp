function showElementAtPosition(elementId, x, y) {
    // 他のフォームを全て非表示にする
    var elements = document.getElementsByClassName("task-edit__form");
    for (var element of elements) {
        if (element.id == elementId) {
            continue;
        }
        element.style.display = 'none';
    }

    // 目的のフォームの表示状態を切り替える
    var element = document.getElementById(elementId);
    element.style.display = ((element.style.display != 'none') ? 'none' : 'block');
    if (element) {
        element.style.left = x + "px";
        element.style.top = y + "px";
    }
}

document.addEventListener('click', function(event) {
    event.stopPropagation(); // イベント伝達を防止する
    if (!event.target.classList.contains('task-edit__btn') && !event.target.classList.contains('task-edit__form__content')) {
        var task_edit__form_elements = document.getElementsByClassName("task-edit__form");
        for (var task_edit__form_element of task_edit__form_elements) {
            task_edit__form_element.style.display = 'none';
        }
    }
});


