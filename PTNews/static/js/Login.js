$(document).ready(function() {
    $('#username, #password').click(function() {
        $("html, body").animate({ scrollTop: $(".container-login").offset().top });
    });
});