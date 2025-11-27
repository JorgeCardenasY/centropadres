
# Proyecto de Gestión para Centro de Padres

Aplicación web desarrollada con **Django** para modernizar, centralizar y simplificar la administración financiera de un Centro de Padres escolar. La plataforma permite gestionar cuotas, deudas, pagos y perfiles de forma transparente para apoderados, tesoreros y administradores.

---

## 🚀 Funcionalidades Principales

- **Gestión de Perfiles**
  - Registro y administración de *apoderados* y *alumnos*.
  - Asociación entre cada alumno y su apoderado responsable.

- **Autenticación de Usuarios**
  - Sistema de inicio de sesión seguro.
  - Cada apoderado accede exclusivamente a su información personal.

- **Gestión Financiera**
  - Creación de *Conceptos de Pago* (ej. “Cuota Anual 2024”, “Paseo de fin de año”).
  - Asignación de deudas a apoderados de forma individual o masiva.
  - Registro detallado de pagos con monto, fecha y método.

- **Control de Acceso por Roles**
  - Permisos diferenciados según tipo de usuario:
    - Apoderado  
    - Apoderado Tesorero  
    - Superusuario (Django Admin)

- **Reportes Financieros**
  - Estado general del curso.
  - Saldos pendientes por apoderado.
  - Monto total recaudado.

- **Panel de Administración Personalizado**
  - Mejoras sobre el *admin* de Django.
  - Carga masiva de alumnos vía archivos CSV.

---

## 👥 Roles de Usuario

El sistema contempla tres tipos de usuarios:

---

### 1. **Apoderado (Usuario Estándar)**

Es el padre, madre o tutor responsable del alumno.

**Permisos y características:**

- Visualizar su perfil en la sección **Mi Perfil**.
- Consultar un resumen de sus deudas:
  - Conceptos asignados.
  - Monto total.
  - Abonos registrados.
  - Saldo pendiente.
- Revisar historial de pagos.
- Acceder a la información de contacto de los *Apoderados Tesoreros*.

---

### 2. **Apoderado Tesorero (Usuario Administrador Financiero)**

Es un apoderado con permisos extendidos, asignados desde el panel de administración.

**Permisos adicionales:**

- Todas las funciones del Apoderado estándar.
- Registrar pagos realizados por cualquier apoderado.
- Crear deudas individuales o masivas para todos los usuarios.
- Generar reportes financieros filtrados.
- Crear, editar y eliminar registros de pago o deudas en caso de error.

> Este rol depende del atributo booleano `registrar_pago` del usuario.  
> Si está en `True`, el usuario adquiere permisos de CRUD sobre los cargos financieros.

---

### 3. **Superusuario (Administrador Completo del Sistema)**

Tiene acceso total a todas las funcionalidades y datos dentro del sistema, además del panel `/admin`.

---

## 🔐 Claves de acceso para pruebas

Estas credenciales son solo para demostración. **No deben usarse en producción.**

### Apoderado
- **Usuario:** `227228342`
- **Contraseña:** `password123`

### Superusuario
- **Usuario:** `root`
- **Contraseña:** `a4t5one3`

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 4.2 (Python)
- **Base de Datos:** PostgreSQL (producción) / SQLite (desarrollo)
- **Frontend:** HTML + CSS + JavaScript con **Bootstrap**
- **Servidor de aplicación:** Gunicorn
- **Servidor de archivos estáticos:** WhiteNoise
- **Dependencias clave:**  
  `django`, `gunicorn`, `dj_database_url`, `psycopg2-binary`, `whitenoise`

---

## 🧩 Estructura del Proyecto

El proyecto está dividido en tres aplicaciones Django:

| Aplicación | Descripción |
|-----------|-------------|
| `centropadres` | Configuración principal del proyecto. |
| `perfiles` | Gestión de apoderados y alumnos. |
| `gestion` | Lógica de Conceptos, Deudas y Registros de Pago. |

---

## ⚙️ Instalación y Puesta en Marcha (Entorno de Desarrollo)

Siga los siguientes pasos para ejecutar el proyecto localmente:

---

### 1. Clonar el repositorio

```bash
git clone https://github.com/JorgeCardenasY/centropadres
cd centropadres
```

---

### 2. Crear y activar un entorno virtual

```bash
python -m venv myenv
source myenv/bin/activate   # En Windows: myenv\Scripts\activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Configurar base de datos (SQLite para desarrollo)

Edite `centropadres/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

---

### 6. Crear un superusuario

```bash
python manage.py createsuperuser
```

---

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en:

👉 http://127.0.0.1:8000/

---

## 📌 Notas del Proyecto

Este proyecto está en **desarrollo activo**. Entre sus futuras extensiones se considera:

- Gestión de actividades y eventos.
- Publicación de comunicados.
- Sistema de mensajería interna.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas mediante *issues* o *pull requests*:

👉 https://github.com/JorgeCardenasY/centropadres

---

## 🧑‍💻 Autor

Proyecto desarrollado por **Jorge Cárdenas**.  
Documentación revisada y ordenada para despliegue en GitHub.
