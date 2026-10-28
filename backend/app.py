from flask import Flask, request, make_response, jsonify
from routes.example import example_bp
import db

app = Flask(__name__)
app.register_blueprint(example_bp)

ALLOWED_IPS = {'127.0.0.1'}
PROTECTED_ENDPOINTS = {'get_blacklist', 'add_to_blacklist', 'remove_from_blacklist'}

@app.before_request
def limit_remote_addr():
    if request.endpoint not in PROTECTED_ENDPOINTS:
        return None  
    if request.remote_addr not in ALLOWED_IPS:
        print(request.remote_addr)
        abort(403)  

@app.route("/api/get_blacklist")
def get_blacklist():
    response = make_response(jsonify(db.get_blacklist()))
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:9000"

    return response

@app.route("/api/add_to_blacklist/<email>", methods=['GET', 'POST'])
def add_to_blacklist(email):
    response = make_response(jsonify(db.add_to_blacklist(email)))
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:9000"

    return response

@app.route("/api/remove_from_blacklist/<email>", methods=['GET', 'POST'])
def remove_from_blacklist(email):
    response = make_response(jsonify(db.remove_from_blacklist(email)))
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:9000"

    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=8000)