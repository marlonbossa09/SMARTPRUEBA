#!/bin/sh
set -e

# El compose gatea el arranque de este contenedor con
# `depends_on: db: condition: service_healthy`, así que para cuando
# llegamos aquí Postgres ya acepta conexiones y no hace falta un
# bucle de espera propio.
echo "Aplicando migraciones de Alembic..."
alembic upgrade head

exec "$@"
