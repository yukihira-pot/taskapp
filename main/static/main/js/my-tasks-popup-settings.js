function toggleVisibility(id) {
    console.log("exe");
    var e = document.getElementById(id);
    e.style.display = ((e.style.display != 'none') ? 'none' : 'block');
}