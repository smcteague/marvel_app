from functools import wraps

import secrets

from flask import request, jsonify, json

from marvel_characters.models import User


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]

        if not token:
            return jsonify({'message': 'Token is missing!'})

        try:
            current_user_token = User.query.filter_by(token = token).first()
            if not current_user_token or current_user_token.token != token:
                return jsonify({'message': 'Token is invalid!'})

        except:
            owner = User.query.filter_by(token = token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid!'})
        
        return our_flask_function(current_user_token, *args, **kwargs)

    return decorated

