from flask import Flask
from routes.example import example_bp
from routes.auth import auth_bp
from verification import build_service_from_env
import db

app = Flask(__name__)
app.register_blueprint(example_bp)
app.register_blueprint(auth_bp)

# Email verification (issue #12). Configured with environment variables;
# see backend/.env.example. With none set it keeps codes in memory and
# prints emails to this terminal, so it works without Postgres or SMTP.
app.extensions["verification_service"] = build_service_from_env()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
