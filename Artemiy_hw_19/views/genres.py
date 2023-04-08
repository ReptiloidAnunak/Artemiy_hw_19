import json
from flask import request
from flask_restx import Resource, Namespace

from models import Genre, GenreSchema
from setup_db import db
from dicorators import admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = json.loads(request.data)
        new_genre = Genre(**req_json)
        db.session.add(new_genre)
        db.session.commit()
        return "", 200, {"location": f"/genres/{new_genre.id}"}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        genre = db.session.query(Genre).get(rid)
        req_json = json.loads(request.data)
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, rid):
        genre = Genre.query.get(rid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204
