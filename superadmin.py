from app import app, db  # Importar la aplicación y la base de datos
from models import Usuario  # Importar el modelo de Usuario

def crear_superadmin():
    # Verificar si ya existe un superadmin
    superadmin = Usuario.query.filter_by(rol='superadmin').first()
    if superadmin:
        print("Ya existe un superadmin.")
        return

    # Crear el superadmin
    nombre = "Maria"
    contraseña = "Arquitectura"  # Cambia esto por una contraseña segura
    superadmin = Usuario(nombre=nombre, rol='superadmin', contraseña=contraseña)
    db.session.add(superadmin)
    db.session.commit()
    print("Superadmin creado correctamente.")

# Ejecutar este script una sola vez
if __name__ == '__main__':
    with app.app_context():  # Usar el contexto de la aplicación
        crear_superadmin()