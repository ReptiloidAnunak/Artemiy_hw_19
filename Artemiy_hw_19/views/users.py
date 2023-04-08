import json

from flask import request
from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')

@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        users_all = User.query.all()
        users = UserSchema(many=True).dump(users_all)
        return users, 200

    def post(self):
        req_json = json.loads(request.data)
        new_user = User(**req_json)
        db.session.add(new_user)
        db.session.commit()
        return "", 200, {"location": f"/movies/{new_user.id}"}


@user_ns.route('/<uid>')
class UserView(Resource):
    def get(self, uid):
        user = User.query.get(uid)
        return UserSchema().dump(user)

    def put(self, uid):
        user = User.query.get(uid)
        req_json = json.loads(request.data)

        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")
        db.session.add(user)
        db.session.commit()
        return "", 204

    def delete(self, uid):
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return "", 204