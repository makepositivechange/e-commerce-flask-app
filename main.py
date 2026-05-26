from flask import Flask, request
from http import HTTPStatus
from db import shops, products
import uuid


app = Flask(__name__)

# shops = [{"name": "Shankar" , "products":[{"name": "Shirt", "price": 1000}, {"name": "Pant", "price": 2000}]}, {"name": "Ravi" , "products":[{"name": "Shirt", "price": 1500}, {"name": "Pant", "price": 2500}]}]

@app.route("/shop", methods = ["GET"])
def get_shops():
    return {"shops" : list(shops.values())}

@app.route("/addshop", methods = ["POST"])
def create_shop():
    shop_data = request.json  
    shops_id = uuid.uuid4().hex
    shop = {**shop_data, "id": shops_id}
    shops[shops_id] = shop
    return {"shop": shop}, HTTPStatus.CREATED


@app.route("/shops/<shop_id>", methods = ["GET"])
def get_shop(shop_id:str):
    try:
        return shops[shop_id], HTTPStatus.OK
    except KeyError:
        return {"message": "Shop not found"}, HTTPStatus.NOT_FOUND

"""
The endpoints from here on is for working on the product database
"""

@app.route("/product", methods = ["POST"])
def add_product():
    new_product = request.json 
    if new_product["shop_id"] not in shops:
        return {"message": "Shop not found"}, HTTPStatus.NOT_FOUND
    product_id = uuid.uuid4().hex
    product = {**new_product, "id": product_id}
    products[product_id] = product

    return product, HTTPStatus.CREATED


@app.route("/product", methods = ["GET"])
def get_products():
    return {"products" : list(products.values())}

@app.route("/products/<product_id>", methods = ["GET"])
def get_product(product_id:str):
    try:
        return products[product_id], HTTPStatus.OK
    except KeyError:
        return {"message": "Product not found"}, HTTPStatus.NOT_FOUND

@app.route("/product/<product_id>", methods = ["DELETE"])
def delete_product(product_id:str):
    try:
        del products[product_id]
        return {"message": "Product deleted successfully"}, HTTPStatus.OK
    except KeyError:
        return {"message": "Product not found"}, HTTPStatus.NOT_FOUND


@app.route("/product/<product_id>", methods = ["PUT"])
def update_product(product_id:str):
    product_data = request.json
    if "price" not in product_data or "name" not in product_data:
        return {"message" : "Please ensure price and product are present in the request body"}, HTTPStatus.BAD_REQUEST
    try:
        product = products[product_id]
        product["name"] = product_data["name"]
        product["price"] = product_data["price"]
        return product, HTTPStatus.OK
    except KeyError:
        return {"message": "Product not found"}, HTTPStatus.NOT_FOUND


app.run()