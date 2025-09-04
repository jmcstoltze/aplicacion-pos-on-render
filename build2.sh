#!/usr/bin/env bash
# build.sh
set -o errexit


# Instalar dependencias
pip install -r requirements.txt


# Colectar archivos estáticos
python manage.py collectstatic --noinput


# Aplicar migraciones
python manage.py makemigrations usuarios
python manage.py makemigrations comercio
python manage.py migrate usuarios
python manage.py migrate comercio
python manage.py migrate


# Crear superusuario
python manage.py createsuperuser --noinput


# Poblar tablas
python manage.py loaddata usuarios/fixtures/auth-users.json
python manage.py loaddata usuarios/fixtures/regiones.json
python manage.py loaddata usuarios/fixtures/comunas.json
python manage.py loaddata usuarios/fixtures/roles.json
python manage.py loaddata usuarios/fixtures/usuarios.json


python manage.py loaddata comercio/fixtures/comercios.json
python manage.py loaddata comercio/fixtures/sucursales.json
python manage.py loaddata comercio/fixtures/bodegas.json
python manage.py loaddata comercio/fixtures/categorias.json
python manage.py loaddata comercio/fixtures/productos.json
python manage.py loaddata comercio/fixtures/stockbodegas.json