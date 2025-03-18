from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from models import db, Producto, Transaccion, Usuario

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://arquitectura:inventarios@localhost/inventarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'arq'
# Inicializar la base de datos y Flask-Login
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Ruta principal
@app.route('/')
def index():
    # Redirigir al login si el usuario no está autenticado
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # Si el usuario está autenticado, mostrar la página principal
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)


# Ruta para agregar producto
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.rol != ['admin','superadmin']:
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

        # Registrar una transacción de entrada
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
    if current_user.rol != 'admin':
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        nuevo_stock = int(request.form['stock'])
        diferencia = nuevo_stock - producto.stock

        # Actualizar el stock del producto
        producto.stock = nuevo_stock
        db.session.commit()

        # Registrar una transacción
        tipo_transaccion = "entrada" if diferencia > 0 else "salida"
        nueva_transaccion = Transaccion(
            tipo=tipo_transaccion,
            fecha=datetime.now(),
            producto_id=producto.id,
            cantidad=abs(diferencia)
        )
        db.session.add(nueva_transaccion)
        db.session.commit()

        flash("Producto actualizado correctamente", "success")
        return redirect(url_for('index'))
    
    return render_template('update_product.html', producto=producto)

# Ruta para eliminar producto
@app.route('/delete/<int:id>')
@login_required
def delete_product(id):
    if current_user.rol != 'admin':
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    producto = Producto.query.get_or_404(id)
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
        contraseña = request.form['contraseña']
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario and usuario.contraseña == contraseña:
            login_user(usuario)
            flash("Inicio de sesión exitoso", "success")

            if usuario.rol in ['admin', 'superadmin']:
                return redirect(url_for('index'))
            else:
                return redirect(url_for('visualizar'))
        else:
            flash("Credenciales incorrectas", "error")
    
    return render_template('login.html')
# Ruta para cerrar sesión
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
        contraseña = request.form['contraseña']

        # Todos los nuevos usuarios se registran como "empleado" por defecto
        nuevo_usuario = Usuario(nombre=nombre, rol='empleado', contraseña=contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/asignar_rol/<int:user_id>', methods=['GET', 'POST'])
@login_required
def asignar_rol(user_id):
    # Solo el superadmin puede asignar roles
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
        db.create_all()
    app.run(debug=True)