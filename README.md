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
* Integridad referencial: al eliminar un proveedor, los productos que tenía asociados no se borran ni quedan corruptos, sino que su identificador se marca como NULL
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

* Incorporar una función para calcular el stock en tiempo real de la cafetería con cada movimiento de los artículos.
* Añadir una función para que avise al usuario de que el stock está al mínimo
* Añadir otra función para la autenticación de usuarios