
import datetime
import calendar
import hashlib
import json

import jwt
from flask import request, abort
from flask_restx import Namespace, Resource
from costants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_SECRET, JWT_ALGORITHM
from models import User, UserSchema
from setup_db import db

auth_ns = Namespace('auth')

def generate_tokens(data, is_refresh=False):
    """Генерирует токены jwt"""
    #Токен доступа на 30 мин
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # Токен доступа на 130 дней
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": access_token, "refresh_token": refresh_token}

@auth_ns.route('/')
class AuthView(Resource):
    """Получает логин и пароль из Body запроса в виде JSON, далее проверяет соотвествие с данными в БД (есть ли такой пользователь, такой ли у него пароль)
и если всё оk — генерит пару access_token и refresh_token и отдает их в виде JSON."""
    def post(self):
        req_json = json.loads(request.data)
        print(req_json)
        username = req_json.get('username', None)
        password = req_json.get('password', None)
        if None in [username, password]:
            return "Нет логина или пароля", 400

        user = User.query.filter(User.username == username).first()

        if user is None:
            raise abort(404)

        if user.compare_password(password) == False:
            return 'Пароль неверный'

        data = {"username": user.username,
                "password" : user.password,
                "role": user.role}

        return generate_tokens(data), 200

    def put(self):
        '''Получает refresh_token из Body запроса в виде JSON, далее проверяет refresh_token и если он не истек и валиден — генерит пару access_token и refresh_token и отдает их в виде JSON.'''
        try:
            data = json.loads(request.data)
            refresh_token = data.get("refresh_token")
            decoded_data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        except Exception as e:
            print('JWT decode exception', e)
            return 'Token is not valid:', 404

        username = decoded_data.get("username")
        data = {"username": username, "password": None}
        return generate_tokens(data, is_refresh=True), 200
