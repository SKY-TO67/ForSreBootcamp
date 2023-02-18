from methods import Token, Restricted
from flask import g, request, Flask, current_app, jsonify
import functools
import datetime

app = Flask(__name__)
login = Token()
protected = Restricted()


# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['GET','POST'])
def url_login():
    username = request.form.get('username')
    password = request.form.get('password')
    res = {
        "data": login.generate_token(username, password)
    }
    return jsonify(res)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected", methods=['GET', 'POST'])
def url_protected():
    auth = request.headers.get('Authorization')
    res = {
        "data": protected.access_data(auth)
    }
    return jsonify(res)

def login_required(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if g.username == 1:
                return {'code': 4001, 'message': 'token is no longer valid'}, 401
            elif g.username == 2:
                return {'code': 4002, 'message': 'token authentication failed'}, 401
            elif g.username == 2:
                return {'code': 4003, 'message': 'Illegal token'}, 401
            else:
                return f(*args, **kwargs)
        except BaseException as e:
            return {'code': 4004, 'message': 'Please login to authenticate first.'}, 401
    return wrapper

# http://127.0.0.1:8000/api/test
#   output: "code": 4001,
#           "message": "Please login to authenticate first."
@app.route('/api/test', methods=['GET', 'POST'])
@login_required
def submit_test_info_():
    username = g.username
    return username

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)