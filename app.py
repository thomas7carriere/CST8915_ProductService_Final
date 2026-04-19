from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv("PORT", 3030))

products = [
    {
        "id": "p1001",
        "name": "Gaming Mouse",
        "category": "Accessories",
        "brand": "Logitech",
        "price": 79.99,
        "stock": 25
    },
    {
        "id": "p1002",
        "name": "Mechanical Keyboard",
        "category": "Accessories",
        "brand": "Keychron",
        "price": 129.99,
        "stock": 15
    },
    {
        "id": "p1003",
        "name": "4K Monitor",
        "category": "Monitors",
        "brand": "Samsung",
        "price": 349.99,
        "stock": 10
    }
]

@app.get("/")
def home():
    return "Product service is running"

@app.get("/products")
def get_products():
    return jsonify(products), 200

@app.get("/products/<product_id>")
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@app.post("/products")
def create_product():
    data = request.get_json()

    required_fields = ["id", "name", "category", "brand", "price", "stock"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    existing_product = next((p for p in products if p["id"] == data["id"]), None)
    if existing_product:
        return jsonify({"error": "Product with this id already exists"}), 409

    products.append(data)
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)