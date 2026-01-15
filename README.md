# TransportNet - Red Social de Transportes

Plataforma web para conectar transportistas y gestionar envíos de mercaderías con autenticación Google.

## Características

- **Red Social**: Publicaciones y conexiones entre usuarios
- **Autenticación Google**: Inicio de sesión seguro con OAuth 2.0
- **Gestión de Envíos**: Registrar mercaderías con volumen, origen, destino y presupuesto
- **Interfaz Web**: Aplicación moderna usando Flask y Bootstrap

## Requisitos

- Python 3.8+
- Flask 2.3+
- SQLAlchemy

## Instalación

1. Clona el repositorio
2. Instala dependencias:
```bash
pip install -r requirements.txt
```

3. Configura variables de entorno en `.env`:
```
SECRET_KEY=tu-clave-secreta
GOOGLE_CLIENT_ID=tu-client-id-de-google
GOOGLE_CLIENT_SECRET=tu-client-secret-de-google
```

4. Ejecuta la aplicación:
```bash
python main.py
```

## Configuración de Google OAuth

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ API
4. Crea credenciales OAuth 2.0
5. Agrega los orígenes autorizados: `http://localhost:5000`
6. Agrega los URI de redireccionamiento: `http://localhost:5000/auth/google/callback`

## Uso

- Accede a `http://localhost:5000`
- Inicia sesión con Google
- Publica en la red social
- Agrega tus envíos de mercaderías

### Inicio de la aplicación (Local)

```bash
python main.py
```

### Inicio con Docker

```bash
docker-compose up
```

O si construiste la imagen manualmente:

```bash
docker run -e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix gestor-empresas
```

La aplicación se divide en 3 pestañas principales:

### 1. Pestaña "Empresas"

Gestiona el registro de empresas.

**Acciones disponibles:**
- **Agregar Empresa**: Ingresa nombre, email, teléfono y dirección
- **Editar**: Modifica los datos de una empresa seleccionada
- **Eliminar**: Elimina una empresa y todos sus empleados asociados

### 2. Pestaña "Empleados"

Gestiona empleados asociados a empresas.

**Acciones disponibles:**
- **Selecciona una empresa** de la lista
- **Agregar Empleado**: Completa nombre, apellido, email, teléfono y posición
- **Editar**: Modifica datos del empleado
- **Eliminar**: Elimina un empleado

**Datos de empleado:**
- Nombre
- Apellido
- Email (para envío de mensajes)
- Teléfono
- Posición/Cargo

### 3. Pestaña "Mensajes"

Crea plantillas y envía mensajes personalizados.

#### Variables dinámicas disponibles

Usa estas variables en tu plantilla para personalizar mensajes:

```
{nombre}           - Nombre del empleado
{apellido}         - Apellido del empleado
{nombre_completo}  - Nombre completo (Nombre Apellido)
{email}            - Email del empleado
{telefono}         - Teléfono del empleado
{posicion}         - Posición/Cargo del empleado
{empresa}          - Nombre de la empresa
```

#### Ejemplo de plantilla

```
Estimado {nombre_completo},

Espero que te encuentres bien. Somos {empresa} y queremos contactarte en tu rol como {posicion}.

Tu email registrado es: {email}
Tu teléfono: {telefono}

Atentamente,
Equipo
```

#### Crear una plantilla

1. En la pestaña "Mensajes"
2. Ingresa un nombre descriptivo (ej: "Mensaje de Bienvenida")
3. Escribe el contenido usando las variables dinámicas
4. Haz clic en "Guardar Plantilla"

#### Enviar mensajes

1. Selecciona una empresa
2. Selecciona una plantilla
3. Haz clic en "Generar Vista Previa" para ver cómo se vería el mensaje personalizado
4. Si deseas copiar los emails de los empleados: haz clic en "Copiar Emails"
5. Configura el email (Gmail u Outlook) haciendo clic en "Configurar Email"
6. Haz clic en "Enviar Emails" para enviar los mensajes personalizados

#### Configuración de Email

**Para Gmail:**
1. Habilita "Contraseñas de aplicación" en tu cuenta de Google (2FA debe estar activo)
2. Genera una contraseña de aplicación
3. Proveedor: Gmail
4. Email: Tu correo de Gmail
5. Contraseña: La contraseña de aplicación generada

**Para Outlook:**
1. Usa tu email y contraseña de Outlook/Microsoft
2. Proveedor: Outlook
3. Email: Tu correo de Outlook
4. Contraseña: Tu contraseña de Outlook

## Estructura de la aplicación

```
├── main.py                 # Punto de entrada
├── config/
│   └── database.py         # Configuración de SQLite
├── models/
│   ├── company.py          # Modelo de Empresa
│   └── employee.py         # Modelo de Empleado
├── db/
│   └── repository.py       # Capa de acceso a datos (CRUD)
├── services/
│   ├── message_service.py  # Procesamiento de plantillas
│   └── email_service.py    # Integración SMTP
├── ui/
│   ├── main_window.py      # Ventana principal
│   ├── dialogs.py          # Diálogos modales
│   └── widgets.py          # Componentes reutilizables
├── database.db             # Base de datos SQLite
└── requirements.txt        # Dependencias Python
```

## Base de datos

Los datos se almacenan en `database.db` (SQLite) que se crea automáticamente.

**Tablas:**
- `companies` - Registro de empresas
- `employees` - Registro de empleados
- `message_templates` - Plantillas de mensajes

## Formato de variables en mensajes

Las variables se escriben entre llaves `{}`. Por ejemplo:

```
Hola {nombre}, tu email es {email}
```

Se convertirá en:

```
Hola Juan, tu email es juan@example.com
```

Si una variable no existe o está vacía, se mostrará como texto vacío.

## Seguridad

- Las contraseñas de email NO se guardan en la base de datos
- Se ingresan cada vez que configuras el email
- Se usan conexiones SMTP TLS (puerto 587)

## Soporte de proveedores de email

- **Gmail** (smtp.gmail.com:587)
- **Outlook** (smtp-mail.outlook.com:587)

## Notas importantes

- Los empleados deben tener un email válido para recibir mensajes
- Las plantillas deben estar creadas antes de enviar mensajes
- Se recomienda generar una vista previa antes de enviar emails masivos
- Todos los empleados de la empresa seleccionada recibirán el mensaje

## Autor

Desarrollado con Python 3.13 y PyQt6
├── models/company.py, employee.py
├── db/repository.py
├── ui/main_window.py, dialogs.py, widgets.py
└── services/message_service.py, email_service.py
```

## Configuración de Email

### Gmail
1. Usar correo de Gmail
2. Generar "Contraseña de aplicación" en https://myaccount.google.com/apppasswords
3. Usar esa contraseña (no la contraseña de la cuenta)

### Outlook
1. Usar correo de Outlook
2. Usar contraseña normal de la cuenta

