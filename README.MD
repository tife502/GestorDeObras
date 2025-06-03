# BACKEND 
# 1. Clonar el repositorio 
 ### git clone  https://github.com/tife502/GestorDeObras.git

 ### cd tu-proyecto 

# 2. Instalamos las dependencias 

     cd tu-proyecto

     python -m venv venv

     pip install -r requirements.txt

# si no existe requirements.txt, puedes crearlo con:

     pip freeze > requirements.txt

# 3. Crea un archivo de entornos con las variables: 

     SECRET_KEY= una_clave_secreta_para_tokens

     DATABASE_URL= URL de la base de datos con postgres

     MAIL_USERNAME=Usuario postgres

     MAIL_PASSWORD= contraseña postgres

# 4. Crea la base de datos postgres: 

     CREATE DATABASE nombre_base_datos;


# 5. Configurar Flask para conectarse a PostgreSQL

    En tu archivo .env (o en config.py):

         DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_base_datos

# 6. Usar Flask-Migrate para generar y aplicar migraciones

    # a) Instalar dependencias: 

       pip install Flask-Migrate

    # b) Inicializar el entorno de migraciones (una sola vez)

       flask db init

       Esto crea una carpeta migrations/.

    # c) Generar las migraciones a partir de tus modelos

         flask db migrate -m "Inicial"

    # d) Aplicar las migraciones (crear las tablas en PostgreSQL)

         flask db upgrade

        # Esto creará automáticamente las tablas definidas en tus modelos Python en la base de datos PostgreSQL (puedes verlas en pgAdmin → Schemas → Tables).

# 7. Ejecutar el backend: 
    python run.py

