from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Base de datos simulada en memoria (diccionario)
inventario = {}

@app.route('/')
def index():
    return render_template('index.html', inventario=inventario)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        inventario[nombre] = inventario.get(nombre, 0) + cantidad
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/update/<string:nombre>', methods=['GET', 'POST'])
def update_product(nombre):
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        if nombre in inventario:
            inventario[nombre] = cantidad
        return redirect(url_for('index'))
    return render_template('update_product.html', nombre=nombre, cantidad=inventario.get(nombre, 0))

@app.route('/delete/<string:nombre>')
def delete_product(nombre):
    if nombre in inventario:
        del inventario[nombre]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
