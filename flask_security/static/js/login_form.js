$(function () {
    $("#form_login").submit(function (e) {
        e.preventDefault();
    }).validate({
        submitHandler: function (form) {
            $.ajax({
                url: form.action,
                type: form.method,
                data: $(form).serialize(),
                success: function (data) {
                    if (data.status == 200) {
                        window.location.replace("/");
                    } else {
                        $.notify(data.message, "error");
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    $.notify(thrownError + "(" + xhr.status + "): " + xhr.responseText, "error");
                }
            })
        }
    });
})