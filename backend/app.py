
from flask import Flask
from flask_cors import CORS
from routes.example import example_bp
from routes.rides import rides_bp
import db

app = Flask(__name__)
CORS(app)

app.register_blueprint(example_bp)
app.register_blueprint(rides_bp)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
