from http import HTTPStatus

from flask.views import MethodView  # pyright: ignore
from flask_smorest import Blueprint, abort  # pyright: ignore
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  # pyright: ignore

from db import db
from models import ShopModel
from schema import ShopSchema

blueprint = Blueprint("shops", __name__, description="Operations on shops")


@blueprint.route("/shops/<shop_id>")
class Shop(MethodView):
    @blueprint.response(HTTPStatus.OK, ShopSchema)
    def get(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        return shop

    def delete(self, shop_id):
        product = ShopModel.query.get_or_404(shop_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Shop deleted successfully"}


@blueprint.route("/shop")
class ShopList(MethodView):
    @blueprint.response(HTTPStatus.OK, ShopSchema(many=True))
    def get(self):
        shops = ShopModel.query.all()
        return shops

    @blueprint.arguments(ShopSchema)
    @blueprint.response(HTTPStatus.CREATED, ShopSchema)
    def post(self, shop_data):
        shop = ShopModel(**shop_data)
        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.BAD_REQUEST, message="Shop with this name already exists")
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while creating the shop",
            )
        return shop
