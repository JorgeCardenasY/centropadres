# Documentación del Proyecto: Centro de Padres "SchoolPay"

## 1. Introducción y Propósito del Proyecto

El proyecto "SchoolPay" es una plataforma web desarrollada en Django, diseñada para facilitar la gestión de finanzas del centro de padres de una institución educativa. El sistema centraliza el seguimiento de deudas, cuotas y pagos de los apoderados, ofreciendo transparencia y eficiencia tanto para los padres como para los administradores (tesoreros y superusuarios).

La plataforma busca reemplazar procesos manuales (como hojas de cálculo o registros en papel) por una base de datos centralizada y accesible, permitiendo a cada apoderado consultar su estado de cuenta en tiempo real y a los tesoreros registrar pagos y generar reportes de manera sencilla.

### Componentes Principales:
- **Gestión de Perfiles:** Maneja la información de apoderados y alumnos.
- **Gestión Financiera:** Administra los "conceptos de pago" (ej. "Cuota Anual 2024", "Paseo de fin de año"), asigna deudas a los apoderados y registra los pagos recibidos.
- **Roles de Usuario:** El sistema define varios niveles de acceso para garantizar que cada usuario solo pueda ver y realizar las acciones que le corresponden.
- **Reportes:** Ofrece vistas consolidadas del estado financiero general.

---

## 2. Casos de Uso por Rol de Usuario

A continuación, se detallan los diferentes roles dentro de la plataforma y las acciones que cada uno puede realizar.

### 2.1. Usuario General (No autenticado)

Cualquier persona que visita el sitio web sin iniciar sesión.

**Casos de uso:**
- **Ver la página de inicio:** Puede acceder a la página principal de la plataforma, que presenta información general sobre el centro de padres.
- **Ver la página de contacto:** Puede ver la información de contacto del centro de padres.
- **Iniciar Sesión:** Tiene acceso al formulario de inicio de sesión (`/login/`) para autenticarse como un usuario registrado (apoderado).

### 2.2. Usuario Apoderado (Autenticado)

Un padre o apoderado que ha sido registrado en el sistema y tiene una cuenta de usuario.

**Casos de uso:**
- **Acceder a "Mi Perfil":** Una vez iniciada la sesión, es redirigido a su perfil personal. Esta es su vista principal.
- **Consultar Estado de Deudas:** En "Mi Perfil", puede ver un resumen detallado de todas sus deudas asociadas:
    - **Concepto de Pago:** El motivo de la deuda (ej. "Cuota Centro de Padres").
    - **Monto Total:** El valor total del concepto.
    - **Monto Pagado:** La suma de todos los pagos registrados para esa deuda.
    - **Monto Pendiente:** La diferencia entre el total y lo pagado.
    - **Estado:** Un indicador visual del estado del pago ("Pendiente", "Parcialmente Pagado", "Pagado").
- **Ver Historial de Actividad:** Puede consultar una línea de tiempo con todos los eventos importantes de su cuenta, como la fecha de creación del perfil y el historial de todos los pagos que ha realizado.
- **Consultar Información del Alumno:** Puede ver el nombre y curso de su hijo/a asociado.
- **Ver Información de Contacto de Tesoreros:** La plataforma le muestra una lista de los "Apoderados Registradores" (Tesoreros), incluyendo su nombre y número de teléfono, para que sepa a quién contactar para realizar un pago.

**Limitaciones:**
- Un apoderado regular solo puede **consultar** su propia información. No puede registrar pagos, modificar deudas ni ver la información de otros apoderados.

### 2.3. Usuario Apoderado Registrador (Tesorero)

Un apoderado que, además de sus funciones normales, tiene el permiso especial de `registrar_pago = True`. Este rol está pensado para los tesoreros del curso o del centro de padres.

**Casos de uso:**
- **Todas las acciones de un Apoderado regular:** Puede ver su propio perfil y estado de cuenta.
- **Registrar Pagos:** Accede a un formulario especial (`/gestion/registrar-pago/`) donde puede registrar un pago recibido por parte de cualquier apoderado del sistema. Debe especificar:
    - El apoderado que paga.
    - El alumno asociado.
    - El concepto del pago.
    - El monto pagado.
    - El método de pago (ej. "Transferencia", "Efectivo").
- **Asignar Deudas (Conceptos de Pago):** Puede acceder a una función para crear una deuda a:
    - Un apoderado específico.
    - **Todos** los apoderados registrados en el sistema a la vez. Esto es útil para asignar cuotas anuales o deudas generales.
- **Generar Reportes Financieros:** Puede ver un reporte general (`/gestion/reporte/`) que lista a todos los apoderados, los montos que deben pagar por un concepto específico, cuánto han pagado y el saldo pendiente. Este reporte se puede filtrar por concepto de pago.
- **Gestionar Pagos Registrados:** Puede ver una lista de todos los pagos que se han registrado en el sistema (`/gestion/pagos/`) y tiene la capacidad de **eliminar** un registro de pago si fue ingresado por error.
- **Listar Conceptos de Pago:** Puede ver la lista de todos los conceptos de pago existentes en el sistema.

### 2.4. Superusuario

El administrador principal del sistema, con acceso total a todas las funcionalidades a través del panel de administración de Django (`/admin/`).

**Casos de uso:**
- **Todas las acciones de los roles anteriores.**
- **Gestión de Usuarios y Apoderados:**
    - Crear, editar y eliminar cuentas de usuario.
    - Asociar cuentas de usuario a perfiles de `Apoderado`.
    - Asignar el rol de "Apoderado Registrador" (Tesorero) marcando la casilla `registrar_pago` en el perfil de un apoderado.
- **Gestión de Alumnos:**
    - Crear, editar y eliminar perfiles de alumnos.
    - Cargar alumnos de forma masiva a través de un archivo CSV.
    - Asociar alumnos a sus respectivos apoderados.
- **Gestión de Conceptos de Pago:**
    - Crear nuevos conceptos de pago (ej. "Cuota Anual 2025").
    - Editar los detalles de un concepto (nombre, monto total, número de cuotas).
    - Eliminar conceptos de pago.
- **Administración del Sitio:**
    - Acceder a dashboards personalizados para gestionar permisos de usuario y ver sesiones activas.
    - Realizar mantenimiento de la base de datos y configuraciones avanzadas del sistema.
- **Resolución de Problemas:** Tiene la capacidad de corregir cualquier dato en el sistema, como una deuda mal asignada o un pago incorrecto que un tesorero no pueda eliminar.

Si desea conocer más detalles o revisar el proyecto por interés en el desarrollo, puede contactarme a mis redes sociales:

[GitHub](https://github.com/JorgeCardenasY) <br>
[LinkedIn](https://www.linkedin.com/in/jorgecardenasy) <br>
[eLabs.cl](mailto:contacto@elabs.cl)
