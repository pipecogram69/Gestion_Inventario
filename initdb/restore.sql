\! echo "Restaurando la base de datos inventarios..."
\i /docker-entrypoint-initdb.d/inventarios.dump
\! echo "Restauración completada."