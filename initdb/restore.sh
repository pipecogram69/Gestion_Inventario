#!/bin/bash

set -e

echo "Restaurando la base de datos inventarios..."
pg_restore -U postgres -d inventarios /docker-entrypoint-initdb.d/inventarios.dump
echo "Restauración completada."