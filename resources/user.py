"""
Receive username and password from the client.
Check if the username already exists.
If it does not,
             1. Encrypt the password.
             2. Add a new UserModel to the database.
             3. Return a success message.
"""

from http import HTTPStatus

from flask.views import MethodView  # pyright: ignore
from flask_jwt_extended import create_access_token  # pyright: ignore
from flask_smorest import Blueprint, abort  # pyright: ignore
from passlib.hash import pbkdf2_sha256  # pyright: ignore
from schemas import UserSchema  # pyright: ignore

from db import db
from models import UserModel

blueprint = Blueprint("Users", __name__, description="Operations on users")


@blueprint.route("/register")
class UserRegister(MethodView):
    @blueprint.arguments(UserSchema)
    @blueprint.response(HTTPStatus.CREATED, message="User registered successfully")
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(HTTPStatus.CONFLICT, message="Username already exists")
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        return HTTPStatus.CREATED


@blueprint.route("/user")
class User(MethodView):
    @blueprint.response(HTTPStatus.OK, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blueprint.route("/login")
class UserLogin(MethodView):
    @blueprint.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Invalid username or password")
