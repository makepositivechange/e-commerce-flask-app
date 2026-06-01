import os

from flask import Flask  # pyright: ignore
from flask_jwt_extended import JWTManager  # pyright: ignore
from flask_smorest import Api  # pyright: ignore

import models  # noqa: F401
from db import db
from resources.product import blueprint as ProductBlueprint
from resources.shop import blueprint as ShopBlueprint
from resources.user import blueprint as UserBlueprint

app = Flask(__name__)

app.config["API_TITLE"] = "Flask E-Commerce API"
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///shop.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "learn_with_pratap"

jwt = JWTManager(app)

db.init_app(app)

api = Api(app)

# Here we create the database tables
with app.app_context():
    db.create_all()

api.register_blueprint(ShopBlueprint)
api.register_blueprint(ProductBlueprint)
api.register_blueprint(UserBlueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)