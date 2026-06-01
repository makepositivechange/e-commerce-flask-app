import os

from flask import Flask, jsonify  # pyright: ignore
from flask_jwt_extended import JWTManager  # pyright: ignore
from flask_smorest import Api  # pyright: ignore

import models  # noqa: F401
from db import db
from resources.product import blueprint as ProductBlueprint
from resources.shop import blueprint as ShopBlueprint
from resources.user import blueprint as UserBlueprint
from http import HTTPStatus
from blacklist import BLACKLIST
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

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_header["jti"] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message":"The token is revoked", 
                     "error":"token_revoked"}), HTTPStatus.UNAUTHORIZED)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message":"The provided token is expired", 
                     "error":"token_expired"}), HTTPStatus.UNAUTHORIZED)

@jwt.invalid_token_loader
def invalid_token_loader_callback(error):
    return (jsonify({"message":"Signature verfication failed", 
                     "error":"invalid_token"}), HTTPStatus.UNAUTHORIZED)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (jsonify({"message":"Request does not contain an access token", 
                    "error":"authorization_required"}), HTTPStatus.UNAUTHORIZED)

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"message":"the token is not fresh", 
                    "error":"fresh_token_required"}), HTTPStatus.UNAUTHORIZED) 

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