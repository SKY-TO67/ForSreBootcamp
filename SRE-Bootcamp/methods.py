from flask import g, request, Flask, current_app, jsonify
import jwt
from jwt import exceptions
import datetime

headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}

SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='


class Token:

    def generate_token(self, username, password):
        payload = {
            'username': username,
            'password': password,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers) # decode('utf-8')
        return result


class Restricted:

    def access_data(self, auth):
        if auth and auth.startswith('Bearer '):
            token = auth[7:]
            g.username = None
            try:
                payload = jwt.decode(token, SALT, algorithms=['HS256'])
                g.username = payload.get('username')
            except exceptions.ExpiredSignatureError:
                g.username = 1
            except jwt.DecodeError:
                g.username = 2
            except jwt.InvalidTokenError:
                g.username = 3

        return 'under protected data'