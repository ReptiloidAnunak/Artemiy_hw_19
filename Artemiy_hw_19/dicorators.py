import jwt
from flask import request, abort
from costants import JWT_SECRET, JWT_ALGORITHM


def auth_requires(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        except Exception as e:
            print("JWT Decode Exception:", e)
            abort(401)

        return func(*args, **kwargs)

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get("role", "user")
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            user_data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user_data.get("role")

            if role != "admin":
                abort(401)

        except Exception as e:
            print("JWT Decode Exception:", e)
            abort(401)


        return func(*args, **kwargs)
    return wrapper