# STOCK CAFETERIA
Aplicación Web diseñada para gestionar el stock de una cafetería
## Tecnologías usadas

* Python
* SQLAlchemy
* SQLite
* Flask
## Funcionalidades

* Gestión de proveedores
* Gestión de productos
* Gestión de movimientos
* Integridad referencial:
  - Al eliminar un proveedor, los productos que tenía asociados no se borran ni quedan corruptos, sino que su identificador se marca como NULL.
  - Al añadir o quitar algún producto, el programa actualiza el stock de ese producto, el programa nos notificará cuál es el 
  - stock actual (current_stock).
  - Al quedarse algún producto sin stock, el código nos devuelve un mensaje notificando que necesita ser repuesto, con un (True o False).
## Instalación
```bash 
git clone https://github.com/ignaciocantero94/inventario-cafeteria.git 
cd inventario-cafeteria 
python3 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt 
python3 app.py
```
## Estructura del modelo de datos

* Tabla Proveedores, representa todos los proveedores de los artículos de la cafetería, tiene datos de contacto y relación 1:N con la tabla Productos.
* Tabla Productos, representa todos los artículos de la cafetería, tiene datos para gestionar el stock mínimo, categoría del producto o el nombre del mismo, tiene relación 1:N con la tabla movimientos.
* Tabla Movimientos, representa todos los movimientos de los artículos de la cafetería, tiene los datos de entrada/salida de productos, la fecha de esa modificación y la cantidad de stock de cada uno.
## Mejoras futuras

* Añadir otra función para la autenticación de usuarios