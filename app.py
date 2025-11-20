from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Base de datos simulada
productos = [
    {
        "id": 1,
        "nombre": "Papa Blanca",
        "productor": "Juan Pérez",
        "ubicacion": "Huancayo",
        "cantidad_kg": 500,
        "precio_kg": 2.50,
        "disponible": True,
        "fecha_registro": "2025-11-15"
    },
    {
        "id": 2,
        "nombre": "Quinua Orgánica",
        "productor": "María Torres",
        "ubicacion": "Puno",
        "cantidad_kg": 200,
        "precio_kg": 8.00,
        "disponible": True,
        "fecha_registro": "2025-11-18"
    }
]

@app.route('/')
def home():
    return jsonify({
        "mensaje": "API TierraConnect",
        "version": "1.0",
        "endpoints": ["/productos", "/productos/<id>", "/productos/disponibles"]
    })

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    producto = next((p for p in productos if p["id"] == producto_id), None)
    if producto:
        return jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/productos/disponibles', methods=['GET'])
def productos_disponibles():
    disponibles = [p for p in productos if p["disponible"]]
    return jsonify({
        "total": len(disponibles),
        "productos": disponibles
    })

@app.route('/productos', methods=['POST'])
def crear_producto():
    nuevo_producto = request.json
    nuevo_producto["id"] = len(productos) + 1
    nuevo_producto["fecha_registro"] = datetime.now().strftime("%Y-%m-%d")
    productos.append(nuevo_producto)
    return jsonify(nuevo_producto), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)