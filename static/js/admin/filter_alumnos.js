document.addEventListener("DOMContentLoaded", function() {
    (function($) {
        $(document).ready(function() {
            var apoderadoSelect = $('#id_apoderado');
            var alumnoSelect = $('#id_alumno');

            apoderadoSelect.on('change', function() {
                var apoderadoId = $(this).val();
                if (apoderadoId) {
                    $.ajax({
                        url: '/gestion/ajax/get-alumnos-for-apoderado/',
                        data: {
                            'apoderado_id': apoderadoId
                        },
                        success: function(data) {
                            var selectedAlumno = alumnoSelect.val();
                            alumnoSelect.empty();
                            alumnoSelect.append($('<option>', {
                                value: '',
                                text: '---------'
                            }));
                            $.each(data.alumnos, function(i, alumno) {
                                alumnoSelect.append($('<option>', {
                                    value: alumno.alumno_id,
                                    text: alumno.nombres + ' ' + alumno.apellidos
                                }));
                            });
                            // Restore selected value if it's still in the list
                            if (selectedAlumno) {
                                alumnoSelect.val(selectedAlumno);
                            }
                        }
                    });
                } else {
                    alumnoSelect.empty();
                    alumnoSelect.append($('<option>', {
                        value: '',
                        text: '---------'
                    }));
                }
            });
            // Trigger change on page load if an apoderado is already selected
            if (apoderadoSelect.val()) {
                apoderadoSelect.trigger('change');
            }
        });
    })(django.jQuery);
});
