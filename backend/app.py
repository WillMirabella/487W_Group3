from flask import Flask
from routes.example import example_bp

app = Flask(__name__)
app.register_blueprint(example_bp)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
