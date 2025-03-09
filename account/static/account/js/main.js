console.log("Working");

$(document).ready(function () {
    setTimeout(function () {
        // Closing the alert after 5 seconds
        $('#alert').alert('close'); // call the Bootstrap's alert('close') method to dismiss it.
    }, 5000);
});

let passwordInputFields = document.querySelectorAll("input[type='password']");
let togglePassword = document.querySelectorAll('.togglePassword'); // get the icon elements

togglePassword.forEach(function (elem) {
    elem.addEventListener('click', function (e) {
        let passwordField = elem.nextElementSibling // Get the immediate next elemment from specific element
        if (passwordField.type === 'password') {
            passwordField.type = 'text'
            elem.classList.replace('fa-eye-slash', 'fa-eye')
        } else {
            passwordField.type = 'password'
            elem.classList.replace('fa-eye', 'fa-eye-slash')
        }
    })
})

