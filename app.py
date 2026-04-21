from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv("PORT", 3030))
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bestbuy")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
products_collection = db["products"]

@app.get("/")
def home():
    return "Product service is running"

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/products")
def get_products():
    products = list(products_collection.find({}, {"_id": 0}))
    return jsonify(products), 200

@app.get("/products/<product_id>")
def get_product(product_id):
    product = products_collection.find_one({"id": product_id}, {"_id": 0})
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@app.post("/products")
def create_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    required_fields = ["id", "name", "category", "brand", "price", "stock"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    existing_product = products_collection.find_one({"id": data["id"]})
    if existing_product:
        return jsonify({"error": "Product with this id already exists"}), 409

    product_to_insert = data.copy()
    products_collection.insert_one(product_to_insert)

    return jsonify(data), 201

@app.put("/products/<product_id>/stock")
def update_stock(product_id):
    data = request.get_json()

    if not data or "stock" not in data:
        return jsonify({"error": "Missing stock value"}), 400

    result = products_collection.update_one(
        {"id": product_id},
        {"$set": {"stock": data["stock"]}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Stock updated"}), 200

if __name__ == "__main__":
    print(f"Product service is running on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)