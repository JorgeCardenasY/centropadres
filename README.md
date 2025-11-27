# Proyecto de Gestión para Centro de Padres

Este proyecto es una aplicación web desarrollada con Django, diseñada para modernizar y simplificar la administración financiera de un centro de padres escolar. La plataforma centraliza la gestión de cuotas, deudas y registros de pago, proporcionando una herramienta transparente y eficiente tanto para los apoderados como para los tesoreros.

## Funcionalidades Principales

- **Gestión de Perfiles:** Administración de apoderados y alumnos, asociando cada alumno a su apoderado correspondiente.
- **Autenticación de Usuarios:** Sistema de login seguro para que cada apoderado acceda a su información privada.
- **Gestión Financiera:**
    - Creación de "Conceptos de Pago" (ej. "Cuota Anual 2024", "Paseo de fin de año").
    - Asignación de deudas a apoderados de forma individual o masiva.
    - Registro detallado de los pagos recibidos.
- **Control de Acceso por Roles:** Funcionalidades diferenciadas según el tipo de usuario (Apoderado, Apoderado Tesorero, Superusuario).
- **Generación de Reportes:** Visualización del estado financiero general del curso, con detalles sobre montos pagados y saldos pendientes por apoderado.
- **Interfaz de Administración Personalizada:** Mejoras sobre el panel de admin de Django para facilitar tareas como la carga masiva de alumnos vía CSV.

---

## Roles de Usuario y Características

El sistema está diseñado para dos tipos de usuarios principales, además del Superusuario de Django.

### 1. Apoderado (Usuario Estándar)

Padre, madre o tutor registrado en el sistema.

- **Consulta de Perfil Propio:** Al iniciar sesión, accede a una página personal ("Mi Perfil").
- **Visualización de Deudas:** Puede ver un resumen claro de todas sus deudas, incluyendo:
    - Concepto de la deuda.
    - Monto total a pagar.
    - Monto ya abonado.
    - Saldo pendiente.
- **Historial de Pagos:** Puede revisar todos los pagos que ha realizado, con fecha y monto.
- **Información de Contacto:** Tiene acceso a los datos de contacto de los "Apoderados Tesoreros" para saber a quién dirigirse para realizar un pago.

### 2. Apoderado Tesorero (Usuario Administrador)

Es un apoderado con permisos especiales para gestionar las finanzas. Este rol se asigna desde el panel de administración.

- **Todas las funcionalidades de un Apoderado.**
- **Registro de Pagos:** Accede a un formulario para registrar los pagos recibidos de cualquier apoderado, especificando el monto, método de pago y concepto.
- **Asignación de Deudas:** Puede crear nuevas deudas (basadas en un "Concepto de Pago") para un apoderado específico o para **todos los apoderados** del sistema de una sola vez.
- **Generación de Reportes Financieros:** Puede visualizar y filtrar un reporte con el estado de cuenta de todos los apoderados, ideal para el seguimiento de la recaudación.
- **Gestión de Registros:** Tiene la capacidad de listar y eliminar registros de pago en caso de error.

---

## Detalles Técnicos

- **Framework Backend:** Django 4.2
- **Lenguaje:** Python
- **Base de Datos:** PostgreSQL (configurado para producción), fácilmente adaptable a SQLite para desarrollo.
- **Frontend:** HTML, CSS y JavaScript, utilizando el framework **Bootstrap** para el diseño responsivo.
- **Servidor de Aplicaciones:** Gunicorn.
- **Servidor de Archivos Estáticos:** WhiteNoise.
- **Dependencias Principales:** `django`, `gunicorn`, `dj_database_url`, `psycopg2-binary`, `whitenoise`.

El proyecto está estructurado en tres aplicaciones de Django:
- `centropadres`: Configuración principal del proyecto.
- `perfiles`: Gestiona los modelos y vistas de `Apoderado` y `Alumno`.
- `gestion`: Contiene la lógica de negocio para `Concepto`, `Deuda` y `RegistroPago`.

## Instalación y Puesta en Marcha

Para ejecutar este proyecto en un entorno de desarrollo local, siga estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-directorio>
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # En Windows: myenv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos:**
    Para desarrollo, puede modificar `centropadres/settings.py` para usar SQLite y evitar la necesidad de un servidor PostgreSQL. Comente la configuración de `DATABASES` existente y descomente o añada la siguiente:
    ```python
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     }
    # }
    ```

5.  **Aplicar las migraciones:**
    ```bash
    python manage.py migrate
    ```

6.  **Crear un superusuario:**
    Este usuario tendrá acceso a todas las funcionalidades del sistema y al panel de administración (`/admin`).
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

La aplicación estará disponible en `http://127.0.0.1:8000/`.
