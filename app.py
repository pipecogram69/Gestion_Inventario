from flask import Flask, render_template, request, redirect, url_for
from models import db, Producto, Transaccion, Usuario

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://arquitectura:inventarios@localhost/inventarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación
db.init_app(app)

# Crear las tablas en la base de datos (solo la primera vez)
with app.app_context():
    db.create_all()

# Ruta principal
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

# Ruta para agregar producto
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')  # Descripción es opcional
        categoria = request.form['categoria']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        # Crear un nuevo producto
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            precio=precio,
            stock=stock
        )

        # Agregar el producto a la base de datos
        db.session.add(nuevo_producto)
        db.session.commit()

        # Redirigir al usuario a la página principal
        return redirect(url_for('index'))
    
    # Si es una solicitud GET, mostrar el formulario
    return render_template('add_product.html')

# Ruta para actualizar producto
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form.get('descripcion', '')
        producto.categoria = request.form['categoria']
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_product.html', producto=producto)

# Ruta para eliminar producto
@app.route('/delete/<int:id>')
def delete_product(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)