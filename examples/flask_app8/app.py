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
