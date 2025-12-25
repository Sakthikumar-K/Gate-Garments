document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const successMsg = document.getElementById("success-message");

    // submit button click
    if (form) {
        form.addEventListener("submit", function () {
            // submit normal ah pogum (preventDefault venda)
        });
    }

    // submit success aana apram popup
    if (successMsg) {
        alert(successMsg.value);
    }

});

window.onload = function () {
    const msg = document.getElementById("django-message");

    if (msg) {
        alert(msg.value);
    }
};
