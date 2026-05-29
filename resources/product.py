import uuid
from http import HTTPStatus

from flask import request  # pyright: ignore
from flask.views import MethodView  # pyright: ignore
from flask_smorest import Blueprint, abort  # pyright: ignore

from db import products
from schema import ProductSchema, ProductUpdateSchema

blueprint = Blueprint("products", __name__, description="Operations on products")


@blueprint.route("/product/<product_id>")
class Product(MethodView):
    def get(self, product_id):
        try:
            return products[product_id], HTTPStatus.OK
        except KeyError:
            abort(HTTPStatus.NOT_FOUND, message="Product not found")

    @blueprint.arguments(ProductUpdateSchema)
    def put(self, product_data, product_id):
        try:
            product = products[product_id]
            # | -> merge the dictionaries
            product |= product_data
            return product, HTTPStatus.OK
        except KeyError:
            abort(HTTPStatus.NOT_FOUND, message="Product not found")

    def delete(self, product_id):
        try:
            del products[product_id]
            return {"message": "Product deleted successfully"}, HTTPStatus.OK
        except KeyError:
            abort(HTTPStatus.NOT_FOUND, message="Product not found")


@blueprint.route("/product")
class Products(MethodView):
    def get(self):
        return {"products": list(products.values())}

    @blueprint.arguments(ProductSchema)
    def post(self, new_product):
        for product in products.values():
            if (
                new_product["name"] == product["name"]
                and new_product["shop_id"] == product["shop_id"]
            ):
                abort(
                    HTTPStatus.BAD_REQUEST,
                    message="Product already exists",
                )
        product_id = uuid.uuid4().hex
        product = {**new_product, "id": product_id}
        products[product_id] = product
        return product
