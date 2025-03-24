import os
from subprocess import call
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from models import db, Producto, Transaccion, Usuario

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://arquitectura:inventarios@localhost/inventarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'arquitectura'  # Clave secreta para manejar sesiones

# Inicializar la base de datos y Flask-Login
db.init_app(app)

# Configurar LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# FUNCIONALIDAD PARA RESTAURAR LA BASE DE DATOS DESDE backup.sql (Se ejecuta automáticamente si no está restaurada)
def restaurar_base_datos():
    # Verificar si ya se restauró la base de datos para evitar restauraciones múltiples
    if not os.path.exists('base_datos_restaurada'):
        print("Restaurando la base de datos desde backup.sql...")
        try:
            # Ejecutar el comando para restaurar el backup usando psql
            call(["psql", "-U", "postgres", "-d", "inventarios", "-f", "backup.sql"])

            # Crear un marcador para evitar restauraciones múltiples
            with open('base_datos_restaurada', 'w') as f:
                f.write("Base de datos restaurada correctamente.")
            print("Base de datos restaurada exitosamente.")
        except Exception as e:
            print(f"Error al restaurar la base de datos: {e}")
    else:
        print("La base de datos ya ha sido restaurada previamente. Omitiendo restauración.")


# Ejecutar la restauración de la base de datos al iniciar la aplicación
with app.app_context():
    restaurar_base_datos()  # Restaurar la base de datos si es necesario
    db.create_all()  # Crear las tablas si no existen


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))



# Ruta principal (redirige al login si no está autenticado)
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Redirigir al login si el usuario no está autenticado
    
    # Si el usuario está autenticado, redirigir según su rol
    if current_user.rol in ['admin', 'superadmin']:
        productos = Producto.query.order_by(Producto.id.asc()).all()  # Ordenar los productos por ID ascendente
        return render_template('index.html', productos=productos)
    else:
        return redirect(url_for('visualizar'))


# Ruta para agregar producto
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.rol not in ['admin', 'superadmin']:
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')
        categoria = request.form['categoria']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            precio=precio,
            stock=stock
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        nueva_transaccion = Transaccion(
            tipo="entrada",
            fecha=datetime.now(),
            producto_id=nuevo_producto.id,
            cantidad=stock
        )
        db.session.add(nueva_transaccion)
        db.session.commit()

        flash("Producto agregado correctamente", "success")
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

# Ruta para actualizar producto
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        # Obtener valores del formulario (si están vacíos, mantener los actuales)
        nuevo_stock = request.form.get('nuevo_stock', '')
        nuevo_precio = request.form.get('nuevo_precio', '')

        # Si el campo de stock no fue modificado, mantén el stock actual
        if nuevo_stock:
            nuevo_stock = int(nuevo_stock)
            diferencia = nuevo_stock - producto.stock
            producto.stock = nuevo_stock

            # Registrar la transacción de stock solo si hay un cambio
            if diferencia != 0:
                tipo_transaccion = "entrada" if diferencia > 0 else "salida"
                nueva_transaccion = Transaccion(
                    tipo=tipo_transaccion,
                    fecha=datetime.now(),
                    producto_id=producto.id,
                    cantidad=abs(diferencia)
                )
                db.session.add(nueva_transaccion)

        # Si el precio no fue modificado, mantener el actual
        if nuevo_precio:
            producto.precio = int(nuevo_precio.replace('.', ''))  # Convertir a entero, eliminando puntos

        db.session.commit()
        db.session.expire_all()  # Forzar actualización de caché

        flash("Producto actualizado correctamente", "success")
        return redirect(url_for('index'))
    
    return render_template('update_product.html', producto=producto)

# Ruta para eliminar producto
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    print(f"Intentando eliminar producto con ID: {id}")  # Debug


    producto = Producto.query.get_or_404(id)

    # Eliminar transacciones relacionadas
    Transaccion.query.filter_by(producto_id=id).delete()


    
    # Eliminar el producto
    db.session.delete(producto)
    db.session.commit()

    flash("Producto eliminado correctamente", "success")
    return redirect(url_for('index'))

# Ruta para ver transacciones
@app.route('/transacciones')
@login_required
def transacciones():
    transacciones = Transaccion.query.all()
    return render_template('transacciones.html', transacciones=transacciones)

@app.route('/usuarios')
@login_required
def lista_usuarios():
    if current_user.rol != 'superadmin':
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    usuarios = Usuario.query.all()
    return render_template('lista_usuarios.html', usuarios=usuarios)

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        print(f"Intento de inicio de sesión: {nombre}")  # Depuración
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario:
            print(f"Usuario encontrado: {usuario.nombre}")  # Depuración
            if usuario.contrasena == contrasena:
                print("Credenciales correctas")  # Depuración
                login_user(usuario)
                flash("Inicio de sesión exitoso", "success")

                if usuario.rol in ['admin', 'superadmin']:
                    print("Redirigiendo a index")  # Depuración
                    return redirect(url_for('index'))
                else:
                    print("Redirigiendo a visualizar")  # Depuración
                    return redirect(url_for('visualizar'))
            else:
                print("Contraseña incorrecta")  # Depuración
                flash("Credenciales incorrectas", "error")
        else:
            print("Usuario no encontrado")  # Depuración
            flash("Credenciales incorrectas", "error")
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('login'))

# Ruta para registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']

        nuevo_usuario = Usuario(nombre=nombre, rol='empleado', contrasena=contrasena)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/asignar_rol/<int:user_id>', methods=['GET', 'POST'])
@login_required
def asignar_rol(user_id):
    if current_user.rol != 'superadmin':
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    usuario = Usuario.query.get_or_404(user_id)
    if request.method == 'POST':
        nuevo_rol = request.form['rol']
        usuario.rol = nuevo_rol
        db.session.commit()
        flash(f"Rol de {usuario.nombre} actualizado a {nuevo_rol}", "success")
        return redirect(url_for('index'))

    return render_template('asignar_rol.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:user_id>')
@login_required
def eliminar_usuario(user_id):
    if current_user.rol != 'superadmin':
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    usuario = Usuario.query.get_or_404(user_id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f"Usuario {usuario.nombre} eliminado correctamente", "success")
    return redirect(url_for('lista_usuarios'))

@app.route('/visualizar')
@login_required
def visualizar():
    if current_user.rol not in ['empleado']:
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    productos = Producto.query.all()
    return render_template('visualizar.html', productos=productos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas si no existen
        app.run(debug=True)