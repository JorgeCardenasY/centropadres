document.addEventListener("DOMContentLoaded", function() {
    (function($) {
        $(document).ready(function() {
            var userSelect = $('#id_user');
            var nombresInput = $('#id_nombres');
            var apellidosInput = $('#id_apellidos');

            userSelect.on('change', function() {
                var userId = $(this).val();
                if (userId) {
                    $.ajax({
                        url: '/perfiles/ajax/get-user-info/',
                        data: {
                            'user_id': userId
                        },
                        success: function(data) {
                            nombresInput.val(data.first_name);
                            apellidosInput.val(data.last_name);
                        }
                    });
                }
            });
        });
    })(django.jQuery);
});
