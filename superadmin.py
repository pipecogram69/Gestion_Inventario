from app import app, db  # Importar la aplicación y la base de datos
from models import Usuario  # Importar el modelo de Usuario
from werkzeug.security import generate_password_hash  # Importar la función de encriptación

def crear_superadmin():
    # Verificar si ya existe un superadmin
    superadmin = Usuario.query.filter_by(rol='superadmin').first()
    if superadmin:
        print("Ya existe un superadmin.")
        return

    # Crear el superadmin con contraseña encriptada
    nombre = "Maria Jose"
    contrasena = "Arqui2025*"  # Cambia esto por una contraseña segura en producción
    
    # Validar que la contraseña cumple los requisitos
    if len(contrasena) < 8:
        print("Error: La contraseña debe tener al menos 8 caracteres")
        return
    
    if not any(c.isupper() for c in contrasena):
        print("Error: La contraseña debe contener al menos una mayúscula")
        return
    
    if not any(c.isdigit() for c in contrasena):
        print("Error: La contraseña debe contener al menos un número")
        return
    
    # Encriptar la contraseña antes de guardarla
    contrasena_encriptada = generate_password_hash(contrasena)
    
    superadmin = Usuario(
        nombre=nombre, 
        rol='superadmin', 
        contrasena=contrasena_encriptada  # Guardar la versión encriptada
    )
    
    db.session.add(superadmin)
    db.session.commit()
    print("Superadmin creado correctamente con contraseña encriptada.")

# Ejecutar este script una sola vez
if __name__ == '__main__':
    with app.app_context():  # Usar el contexto de la aplicación
        crear_superadmin()