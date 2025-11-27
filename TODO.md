# TODO:
Falta Agregar acá descripción de los perfiles de los usuarios

Expplicar en la documetnación que en panel de administración, se debe explicar que los usuario creados builk(csv) automáticamente le crea contraseña password123, . si es manual, se debe crear un usuario, y luego crearlo como apoderado.

---

## Potencialidades de Mejora y Ampliación

### Seguridad
- [ ] **Contraseñas Seguras:** Eliminar la contraseña por defecto (`password123`) para la carga masiva. Implementar un sistema de reseteo de contraseña por correo electrónico para que los usuarios establezcan su propia clave segura en el primer inicio de sesión.
- [ ] **Gestión de Sesiones:** Mejorar la seguridad de las sesiones, incluyendo timeouts y la opción para los usuarios de ver y cerrar sesiones activas desde su perfil.
- [ ] **Permisos Detallados:** Revisar y refinar los grupos y permisos de Django para asegurar que los distintos roles (admin, apoderado) tengan acceso únicamente a las funcionalidades que les corresponden.

### Experiencia de Usuario (UX)
- [ ] **Feedback en Carga de Archivos:** Mejorar la interfaz de carga de CSVs (`upload_csv.html`) para mostrar una barra de progreso, validación de datos en tiempo real y un reporte de errores más claro si la importación falla para filas específicas.
- [ ] **Interfaz Moderna:** Actualizar el diseño de la interfaz (CSS/JS) para que sea más moderno y responsivo (adaptable a móviles), utilizando una versión más reciente de Bootstrap o un framework CSS alternativo.
- [ ] **Perfil de Usuario Enriquecido:** Ampliar la página `mi_perfil.html` para que el apoderado pueda ver un historial de pagos más detallado, gráficos de gastos y gestionar la información de sus alumnos asociados.

### Nuevas Funcionalidades
- [ ] **Integración de Pasarela de Pagos:** Conectar el sistema con una pasarela de pagos online (ej. Stripe, PayPal, MercadoPago) para permitir que los apoderados realicen pagos directamente desde la plataforma en lugar de solo registrarlos.
- [ ] **Módulo de Comunicación:** Crear un sistema de mensajería interna o de anuncios para que la administración pueda comunicarse de forma directa y masiva con los apoderados.
- [ ] **Sistema de Notificaciones:** Enviar notificaciones automáticas por correo electrónico para recordar fechas de vencimiento de pagos, confirmar pagos recibidos o informar sobre nuevas deudas.
- [ ] **Reportes Avanzados:** Expandir la sección de reportes (`reporte_curso.html`) para incluir filtros por fecha, conceptos de pago y alumnos. Añadir la capacidad de exportar reportes en formatos como PDF y Excel.
- [ ] **Módulo de Eventos:** Añadir un calendario de eventos escolares para mantener informados a los padres sobre actividades, reuniones y fechas importantes.

### Calidad de Código y Mantenimiento
- [ ] **Aumentar Cobertura de Pruebas:** Escribir tests unitarios y de integración más completos para las aplicaciones `gestion` y `perfiles` para garantizar la fiabilidad del código y evitar regresiones.
- [ ] **CI/CD (Integración y Despliegue Continuo):** Configurar un pipeline de CI/CD (usando GitHub Actions, GitLab CI, etc.) para automatizar la ejecución de tests y el despliegue de la aplicación a producción.
- [ ] **Revisión de Dependencias:** Auditar el archivo `requirements.txt` para actualizar paquetes obsoletos que puedan tener vulnerabilidades o problemas de rendimiento.
- [ ] **Documentación Técnica:** Mejorar `DOCUMENTACION.md` con instrucciones detalladas para la instalación del entorno de desarrollo, el despliegue en un servidor de producción y la descripción de la arquitectura del proyecto.