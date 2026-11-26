from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields, validate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["JWT_SECRET_KEY"] = "jwt-test-secret-that-is-long-enough-32b"
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(40))


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=4))
    age = fields.Int(load_default=18)


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()


with app.app_context():
    db.create_all()


@app.route("/register", methods=["POST"])
def register():
    try:
        data = RegisterSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    if User.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "exists"}), 409
    u = User(name=data["name"], password=data["password"])
    db.session.add(u)
    db.session.commit()
    return jsonify({"user": UserSchema().dump(u), "age": data["age"]}), 201


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    u = User.query.filter_by(name=body.get("name")).first()
    if u is None or u.password != body.get("password"):
        return jsonify({"msg": "bad credentials"}), 401
    return jsonify(access_token=create_access_token(identity=str(u.id)), refresh_token=create_refresh_token(identity=str(u.id)))


@app.route("/me")
@jwt_required()
def me():
    u = db.session.get(User, int(get_jwt_identity()))
    return jsonify(UserSchema().dump(u))


@app.route("/maybe")
@jwt_required(optional=True)
def maybe():
    return jsonify({"who": get_jwt_identity()})


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return jsonify(access_token=create_access_token(identity=get_jwt_identity()), type=get_jwt()["type"])
