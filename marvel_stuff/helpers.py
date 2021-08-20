from functools import wraps
import secrets

from flask import json, request, jsonify
from marvel_stuff.models import User

def token_required(my_flask_function):
    @wraps(my_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split('')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'})
        
        try:
            current_user_token = User.query.filter_by(token= token).first()
        except:
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Invaild token!'})


        return my_flask_function(current_user_token, *args, **kwargs)
    return decorated

import decimal

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)




