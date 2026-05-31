import uuid
from http import HTTPStatus

from flask.views import MethodView  # pyright: ignore
from flask_smorest import Blueprint, abort  # pyright: ignore

from db import shops
from schema import ShopSchema

blueprint = Blueprint("shops", __name__, description="Operations on shops")


@blueprint.route("/shops/<shop_id>")
class Shop(MethodView):
    @blueprint.response(HTTPStatus.OK, ShopSchema)
    def get(self, shop_id):
        try:
            return shops[shop_id], HTTPStatus.OK
        except KeyError:
            abort(404, message="Shop not found")

    def delete(self, shop_id):
        try:
            del shops[shop_id]
            return {"message": "shop deleted"}, HTTPStatus.OK
        except KeyError:
            abort(404, message="Shop not found")


@blueprint.route("/shop")
class ShopList(MethodView):
    @blueprint.response(HTTPStatus.OK, ShopSchema(many=True))
    def get(self):
        return list(shops.values())

    @blueprint.arguments(ShopSchema)
    @blueprint.response(HTTPStatus.CREATED, ShopSchema)
    def post(self, shop_data):
        for shop in shops.values():
            if shop["name"] == shop_data["name"]:
                abort(HTTPStatus.BAD_REQUEST, message="Shop already exists")
        shops_id = uuid.uuid4().hex
        shop = {**shop_data, "id": shops_id}
        shops[shops_id] = shop
        return shop
