from flask import Flask  # pyright: ignore
from flask_smorest import Api  # pyright: ignore

from resources.product import blueprint as ProductBlueprint
from resources.shop import blueprint as ShopBlueprint

app = Flask(__name__)

app.config["API_TITLE"] = "Flask E-Commerce API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"


api = Api(app)
api.register_blueprint(ShopBlueprint)
app.register_blueprint(ProductBlueprint)
