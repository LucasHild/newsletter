import jwt
from flask import jsonify, request
from functools import wraps

import config


def login_required(f):
    """Decorator checks whether user is logged in"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if "Authorization" in request.headers:
            # Check whether token was sent
            authorization_header = request.headers["Authorization"]

            # Check whether token is valid
            try:
                token = authorization_header.split(" ")[1]
                data = jwt.decode(token, config.secret_key)
                if data["username"] != config.web_username:
                    return jsonify({"error": "Token is invalid"}), 401
            except jwt.exceptions.DecodeError:
                return jsonify({"error": "Token is invalid"}), 401

            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Token is invalid"}), 401
    return wrap


def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username == config.web_username and password == config.web_password:
        token = jwt.encode({"username": username}, config.secret_key)
        return jsonify({"token": token.decode("UTF-8")})
    else:
        return jsonify({"error": "Wrong password or username!"}), 401
