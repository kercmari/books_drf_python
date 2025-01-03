### Libros API
¡Bienvenido a la API de Gestión de Libros! Esta aplicación permite gestionar una colección de libros, incluyendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y obtener estadísticas como el precio promedio de los libros publicados en un año específico.

##### 🚀 Características
* Autenticación JWT: Seguridad en las operaciones mediante tokens JWT.
* CRUD de Libros: Crear, leer, actualizar y eliminar libros.
* Estadísticas: Obtener el precio promedio de libros publicados en un año específico.
* Documentación Swagger: Interfaz interactiva para probar y entender los endpoints de la API.
* Dockerizado: Fácil despliegue y aislamiento del entorno con Docker y Docker Compose.
* Pruebas Automatizadas: Asegura la calidad del código mediante pruebas unitarias.

##### 📦 Instalación y Configuración

1. Clonar el Repositorio  
Abre tu terminal y ejecuta:
```bash
git clone https://github.com/kercmari/books_drf_python.git
```
1. Configurar Variables de Entorno
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

```

SECRET_KEY=django-insecure-g0!iio=-kffxt!7q#!00c#u3k-^tit!zki4gg2k2ob)o($9xad
DEBUG=True
ALLOWED_HOSTS=*

# MongoDB
MONGO_DB_NAME=prueba
MONGODB_URI=mongodb+srv://kerly:holamundo@test.lvmbh.mongodb.net/prueba?retryWrites=true&w=majority&appName=test

```

Notas: * Reemplaza <usuario> y <contraseña> con tus credenciales reales de MongoDB Atlas. * Asegúrate de que tu IP esté permitida en las reglas de acceso de MongoDB Atlas.

3. Construir las Imágenes Docker
Desde la raíz del proyecto, ejecuta:
    ```
    docker compose build --no-cache
    ```
4. Levantar los Contenedores
Inicia los servicios definidos en docker-compose.yml:
    ```bash
       docker compose up
    ```

##### 🧭 Uso
1. Acceder a la API
    * Página Principal:
        ◦ http://localhost:8000/
    * Documentación Swagger:
        ◦ http://localhost:8000/swagger/
2. Endpoints Principales
    * Autenticación:
        - POST /api/users/token/: Obtener tokens de acceso y refresco.
    * Gestión de Libros:
        - GET /api/books/: Obtener una lista paginada de libros.
        - POST /api/books/: Crear un nuevo libro.
        - GET /api/books/<id>/: Obtener detalles de un libro específico.
        - PUT /api/books/<id>/: Actualizar un libro específico.
        - DELETE /api/books/<id>/: Eliminar un libro específico.
    * Estadísticas:
        - GET /api/books/average-price/<year>/: Obtener el precio promedio de libros publicados en un año.

##### 🧪 Ejecutar Pruebas

1. Asegurarse de que los Contenedores Están Parados
Antes de ejecutar las pruebas, detén cualquier contenedor en ejecución:

    ```
    docker-compose down --remove-orphans
    ```
1. Reconstruir las Imágenes Docker
Para asegurarte de que los cambios recientes se reflejen:
    ```
    docker-compose build --no-cache
    ```
1. Ejecutar las Pruebas
Ejecuta las pruebas dentro del servicio web:
    ```
    docker-compose run web python manage.py test
    ```