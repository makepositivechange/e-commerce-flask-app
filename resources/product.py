from http import HTTPStatus

from flask.views import MethodView  # pyright: ignore
from flask_smorest import Blueprint, abort  # pyright: ignore
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  # pyright: ignore

from db import db
from models import ProductModel
from schema import ProductSchema, ProductUpdateSchema

blueprint = Blueprint("products", __name__, description="Operations on products")


@blueprint.route("/product/<product_id>")
class Product(MethodView):
    @blueprint.response(HTTPStatus.OK, ProductSchema)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product

    # Please be careful when we have this decorator as the order is very important
    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(HTTPStatus.OK, ProductSchema)
    def put(self, product_data, product_id):
        product = ProductModel.query.get_or_404(product_id)
        if product:
            product.price = product_data["price"]
            product.name = product_data["name"]
        else:
            product = ProductModel(id=product_id, **product_data)
        try:
            db.session.add(product)
            db.session.commit()
            return product
        except SQLAlchemyError:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, "Deleting is not implemented")
        return product

    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}


@blueprint.route("/product")
class Products(MethodView):
    @blueprint.response(HTTPStatus.OK, ProductSchema(many=True))
    def get(self):
        products = ProductModel.query.all()
        return products

    @blueprint.arguments(ProductSchema)
    @blueprint.response(HTTPStatus.OK, ProductSchema)
    def post(self, new_product):
        product = ProductModel(**new_product)
        try:
            db.session.add(product)  # this is where the product is added to the session
            db.session.commit()
        except IntegrityError:
            abort(
                HTTPStatus.BAD_REQUEST, message="Product with this name already exists"
            )
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while creating the product",
            )

        return product
