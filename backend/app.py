from flask import Flask, request, make_response, jsonify
from routes.example import example_bp
import db

app = Flask(__name__)
app.register_blueprint(example_bp)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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
    app.run(debug=True,port=8000)