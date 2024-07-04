$(document).ready(function() {
    $(document).on('click', '.eye-icon', function() {
        var passwordInput = $('#password');
        var eyeIcon = $(this);

        if (passwordInput.attr('type') === 'password') {
            passwordInput.attr('type', 'text');
            eyeIcon.attr('src', '../static/images/view.png');
        } else {
            passwordInput.attr('type', 'password');
            eyeIcon.attr('src', '../static/images/hidden.png');
        }
    });
});