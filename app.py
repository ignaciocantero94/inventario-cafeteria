from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

"""Todo este proyecto empieza con la terminal, tenemos que, a partir de nuestro servidor Flask y un entorno virtual que
tenemos que crear para ello (venv), añadir cada una de las funciones que tenemos con el comando 'curl', todo para que 
estos datos queden guardados en nuestro servidor web."""

"""Flask es una libreria donde encontramos todo lo necesario para "montar" un servidor, tenemos que hacer una configuración 
previa de flask en la terminal, pero una vez instalada en el PC al usarla aqui estamos indicando que vamos a interactuar con
ese servidor."""

"""Todos los elementos que veamos con db.() se refiere a la biblioteca de SQLAlchemy, una vez que escribes db.() 
estariamos "abriendo una caja" para indicar que queremos usar las sentencias SQL en este caso, por cierto, db 
se usa de modo predeterminado, pero puedes usar otra palabra."""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
db = SQLAlchemy(app)

"""Todo esto son las tablas de nuestra base de datos"""
class Product (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    unit = db.Column(db.String(100))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', ondelete = 'SET NULL'))
    minimum_stock = db.Column(db.Integer)

class Movement (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    movement_type = db.Column(db.String(100))

class Supplier (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))

"""Aqui estamos usando para esta funcion el metodo POST, es lo que necesitamos poner para decirle al programa
que queremos crear o añadir algun elemento."""
@app.route("/supplier", methods = ['POST'])
def create_supplier():
    new_supplier = Supplier(
        name = request.form['name'],
        email = request.form['email'],
        phone = request.form['phone']
    )
    db.session.add(new_supplier)
    db.session.commit()
    return "Supplier added"

"""En esta funcion no añadimos GET, que seria lo que necesitamos para obtener el supplier, por que
al definir "@app.route()" se declara por defecto GET."""
@app.route("/supplier")
def get_supplier():
    suppliers = Supplier.query.all()
    result = []
    for supplier in suppliers:
        result.append({"id": supplier.id, "name": supplier.name, "email": supplier.email, "phone": supplier.phone})
    return jsonify(result)

"""Esta funcion nos permite actualizar los datos de la tabla, por eso usamos el PUT, todo el tema del if nos sirve para
crear la condicion en el caso de que queramos modificar un proveedor que no exista, de ahi el None."""
@app.route("/supplier/<int:id>", methods = ['PUT'])
def update_supplier(id):
    supplier = Supplier.query.get(id)
    if supplier is None:
        return "Supplier not found", 404
    else:
        supplier.name = request.form['name']
        supplier.email = request.form['email']
        supplier.phone = request.form['phone']
        db.session.commit()
        return "Supplier modified"

"""Aqui estamos creando una funcion para eliminar los datos de la tabla, simplemente hay que poner el if para confirmar
que le estamos indicando al programa que elimine a un proveedor que realmente existe."""
@app.route("/supplier/<int:id>", methods = ['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if supplier is None:
        return "An unexisting supplier, it cannot be deleted", 404
    else:
        db.session.delete(supplier)
        db.session.commit()
        return "Supplier deleted"

"""El jsonify es como un traductor, la idea de esto es que los objetos (datos) se muestren en una página web, Python por sí
mismo no puede mostrar esos objetos como texto, necesitamos un modo de traducirlo para que el archivo HTML sepa interpretar 
esos datos, para esto usamos JSON que es un formato de texto compatible con todos los navegadores y pueden usarlo todos 
los EDs."""
@app.route("/product", methods = ['POST'])
def create_product():
    new_product = Product(
        name = request.form['name'],
        category = request.form['category'],
        unit = request.form['unit'],
        supplier_id = request.form['supplier_id'],
        minimum_stock = request.form['minimum_stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return "Product added"

@app.route("/product")
def get_product():
    products = Product.query.all()
    result = []
    for product in products:
        result.append({"id": product.id, "name": product.name, "category": product.category, "unit": product.unit,
                          "supplier_id": product.supplier_id, "minimum_stock": product.minimum_stock})
    return jsonify(result)

"""Despues de cada PUT, tenemos que ir a la terminal y añadir la funcionalidad de modificacion a nuestro server con el 
comando "curl". """
@app.route("/product/<int:id>", methods = ['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if product is None:
        return "Product not found", 404
    else:
        product.name = request.form['name']
        product.category = request.form['category']
        product.unit = request.form['unit']
        product.supplier_id = request.form['supplier_id']
        product.minimum_stock = request.form['minimum_stock']
        db.session.commit()
        return "Product modified"

@app.route("/product/<int:id>", methods = ['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return "An unexisting product, it cannot be removed", 404
    else:
        db.session.delete(product)
        db.session.commit()
        return "Product deleted"

@app.route("/movement", methods = ['POST'])
def create_movement():
    new_movement = Movement(
        product_id = request.form['product_id'],
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
        quantity = request.form['quantity'],
        movement_type = request.form['movement_type']
    )
    db.session.add(new_movement)
    db.session.commit()
    return "Movement complete"

@app.route("/movement")
def get_movement():
    movements = Movement.query.all()
    result = []
    for movement in movements:
        result.append({"id": movement.id, "product_id": movement.product_id, "date": movement.date,
                          "quantity": movement.quantity, "movement_type": movement.movement_type})
    return jsonify(result)

@app.route("/movement/<int:id>", methods = ['PUT'])
def update_movement(id):
    movement = Movement.query.get(id)
    if movement is None:
        return "Movement not found", 404
    else:
        movement.product_id = request.form['product_id']
        movement.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        movement.quantity = request.form['quantity']
        movement.movement_type = request.form['movement_type']
        db.session.commit()
        return "Movement completed"

@app.route("/movement/<int:id>", methods = ['DELETE'])
def delete_movement(id):
    movement = Movement.query.get(id)
    if movement is None:
        return "A movement that was not done, it cannot be discarded", 404
    else:
        db.session.delete(movement)
        db.session.commit()
        return "Movement discarded"

"""Esta función nos sirve para obtener el stock real de cada producto. Lo hace restando la cantidad de artículos que 
entran ('in') menos la cantidad de artículos que salen ('out'). Los valores de acepta movement.movement_type son: 'in/out'"""
@app.route("/product/<int:id>/stock")
def get_stock(id):
    movements = Movement.query.filter_by(product_id=id).all()
    current_stock = 0
    product = Product.query.get(id)
    for movement in movements:
        if movement.movement_type == "in":
            current_stock += movement.quantity
        else:
            current_stock -= movement.quantity
    if current_stock <= product.minimum_stock:
        refill = True
    else:
        refill = False
    return jsonify({"product_id": id, "current_stock": current_stock, "needs_refill": refill})

"""Esto de aqui nos sirve para que el servidor siga en funcionamiento, es necesario en el momento que
invocamos Flask."""
with app.app_context(): db.create_all()

if __name__== "__main__":
    app.run(debug=True)
