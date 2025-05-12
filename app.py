import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, Producto, Transaccion, Usuario
from werkzeug.security import generate_password_hash, check_password_hash  # Añade esto
app = Flask(__name__)

# Configuración de la aplicación
# =============================

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://arquitectura:inventarios@localhost/inventarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'arquitectura'  # Clave secreta para manejar sesiones

# Inicialización de extensiones
db.init_app(app)

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Funciones auxiliares
# ====================

@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario para Flask-Login"""
    return Usuario.query.get(int(user_id))

def registrar_transaccion(tipo, producto_id, cantidad):
    """Registra una transacción en la base de datos"""
    nueva_transaccion = Transaccion(
        tipo=tipo,
        fecha=datetime.now(),
        producto_id=producto_id,
        cantidad=cantidad
    )
    db.session.add(nueva_transaccion)

def verificar_permisos(roles_permitidos):
    """Verifica si el usuario actual tiene los permisos necesarios"""
    if current_user.rol not in roles_permitidos:
        flash("No tienes permisos para acceder a esta página", "error")
        return False
    return True

# Rutas de autenticación
# ======================

@app.route('/')
def index():
    """Página principal - Redirige al login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario and check_password_hash(usuario.contrasena, contrasena):  # Cambia esta línea
            login_user(usuario)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('inventario'))
        
        flash("Credenciales incorrectas", "error")
        return redirect(url_for('login'))
    
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de nuevos usuarios (solo para empleados)"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form.get('confirmar_contrasena', '')
        
        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(nombre=nombre).first()
        if usuario_existente:
            flash("El nombre de usuario ya está en uso", "error")
            return redirect(url_for('registro'))
        
        # Validaciones de contraseña
        if contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('registro'))
        
        if len(contrasena) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "error")
            return redirect(url_for('registro'))
        
        if not any(c.isupper() for c in contrasena):
            flash("La contraseña debe contener al menos una mayúscula", "error")
            return redirect(url_for('registro'))
        
        if not any(c.isdigit() for c in contrasena):
            flash("La contraseña debe contener al menos un número", "error")
            return redirect(url_for('registro'))
        
        # Encriptar la contraseña antes de guardarla
        contrasena_encriptada = generate_password_hash(contrasena)
        
        nuevo_usuario = Usuario(
            nombre=nombre, 
            rol='empleado', 
            contrasena=contrasena_encriptada
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/inventario')
@login_required
def inventario():
    """Página principal del inventario"""
    if current_user.rol not in ['admin', 'superadmin']:
        return redirect(url_for('visualizar'))
    
    # Obtener parámetros de filtro y ordenamiento
    categoria_filtro = request.args.get('categoria', '')
    orden_stock = request.args.get('orden_stock', '')
    
    # Consulta base
    query = Producto.query
    
    # Aplicar filtro si se especificó
    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)
    
    # Aplicar ordenamiento por stock
    if orden_stock == 'mayor':
        query = query.order_by(Producto.stock.desc())
    elif orden_stock == 'menor':
        query = query.order_by(Producto.stock.asc())
    else:
        # Orden por defecto (ID ascendente)
        query = query.order_by(Producto.id.asc())
    
    productos = query.all()
    
    # Obtener todas las categorías únicas para el filtro
    categorias = db.session.query(Producto.categoria).distinct().order_by(Producto.categoria).all()
    categorias = [cat[0] for cat in categorias]
    
    return render_template('inventario.html', 
                        productos=productos,
                        categorias=categorias,
                        categoria_filtro=categoria_filtro,
                        orden_stock=orden_stock)

@app.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario"""
    logout_user()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('login'))



# Rutas de gestión de productos
# =============================

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Añade un nuevo producto al inventario"""
    if not verificar_permisos(['admin', 'superadmin']):
        return redirect(url_for('inventario'))

    if request.method == 'POST':
        nuevo_producto = Producto(
            nombre=request.form['nombre'],
            descripcion=request.form.get('descripcion', ''),
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock'])
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        registrar_transaccion("entrada", nuevo_producto.id, nuevo_producto.stock)
        db.session.commit()

        flash("Producto agregado correctamente", "success")
        return redirect(url_for('inventario'))
    
    return render_template('add_product.html')

@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    """Actualiza un producto existente"""
    if not verificar_permisos(['admin', 'superadmin']):
        return redirect(url_for('inventario'))

    producto = Producto.query.get_or_404(product_id)

    if request.method == 'POST':
        if 'nuevo_stock' in request.form and request.form['nuevo_stock']:
            nuevo_stock = int(request.form['nuevo_stock'])
            diferencia = nuevo_stock - producto.stock
            producto.stock = nuevo_stock

            if diferencia != 0:
                tipo = "entrada" if diferencia > 0 else "salida"
                registrar_transaccion(tipo, producto.id, abs(diferencia))

        if 'nuevo_precio' in request.form and request.form['nuevo_precio']:
            producto.precio = float(request.form['nuevo_precio'])

        db.session.commit()
        flash("Producto actualizado correctamente", "success")
        return redirect(url_for('inventario'))
    
    return render_template('update_product.html', producto=producto)

@app.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Elimina un producto y registra la transacción correspondiente"""
    if not verificar_permisos(['admin', 'superadmin']):
        return redirect(url_for('inventario'))

    producto = Producto.query.get_or_404(product_id)
    
    if producto.stock > 0:
        registrar_transaccion("salida", producto.id, producto.stock)
    
    Transaccion.query.filter_by(producto_id=product_id).delete()
    db.session.delete(producto)
    db.session.commit()

    flash("Producto eliminado correctamente", "success")
    return redirect(url_for('inventario'))

# Rutas de visualización
# ======================

@app.route('/visualizar')
@login_required
def visualizar():
    """Vista de solo lectura para empleados"""
    if not verificar_permisos(['empleado']):
        return redirect(url_for('inventario'))

    productos = Producto.query.all()
    return render_template('visualizar.html', productos=productos)

@app.route('/transacciones')
@login_required
def transacciones():
    """Muestra el historial de transacciones"""
    if not verificar_permisos(['admin', 'superadmin']):
        return redirect(url_for('inventario'))

    transacciones = Transaccion.query.all()
    return render_template('transacciones.html', transacciones=transacciones)

# Rutas de gestión de usuarios
# ============================

@app.route('/usuarios')
@login_required
def lista_usuarios():
    """Lista todos los usuarios (solo superadmin)"""
    if not verificar_permisos(['superadmin']):
        return redirect(url_for('inventario'))

    usuarios = Usuario.query.all()
    return render_template('lista_usuarios.html', usuarios=usuarios)

@app.route('/asignar_rol/<int:user_id>', methods=['GET', 'POST'])
@login_required
def asignar_rol(user_id):
    """Cambia el rol de un usuario (solo superadmin)"""
    if not verificar_permisos(['superadmin']):
        return redirect(url_for('inventario'))

    usuario = Usuario.query.get_or_404(user_id)
    if request.method == 'POST':
        usuario.rol = request.form['rol']
        db.session.commit()
        flash(f"Rol de {usuario.nombre} actualizado a {usuario.rol}", "success")
        return redirect(url_for('inventario'))

    return render_template('asignar_rol.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:user_id>')
@login_required
def eliminar_usuario(user_id):
    """Elimina un usuario (solo superadmin)"""
    if not verificar_permisos(['superadmin']):
        return redirect(url_for('inventario'))

    usuario = Usuario.query.get_or_404(user_id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f"Usuario {usuario.nombre} eliminado correctamente", "success")
    return redirect(url_for('lista_usuarios'))

# Inicialización de la aplicación
# ==============================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)