import json
from flask import request
from flask_restx import Resource, Namespace

from models import Director, DirectorSchema
from setup_db import db
from dicorators import auth_requires, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_requires
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = json.loads(request.data)
        new_dir = Director(**req_json)
        db.session.add(new_dir)
        db.session.commit()
        return "", 200, {"location": f"/directors/{new_dir.id}"}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_requires
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        director = Director.query.get(rid)
        req_json = json.loads(request.data)
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, rid):
        director = Director.query.get(rid)
        db.session.delete(director)
        db.session.commit()
        return "", 204