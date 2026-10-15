from flask import Flask
from routes.example import example_bp
from routes.auth import auth_bp
from verification import build_service_from_env
import db

app = Flask(__name__)
app.register_blueprint(example_bp)
app.register_blueprint(auth_bp)

# email verification (issue #12), settings come from .env (see .env.example)
# with no .env it keeps codes in memory and prints emails here, so no db or email account needed
app.extensions["verification_service"] = build_service_from_env()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
