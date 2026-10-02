from flask import Blueprint, jsonify, request

# make a blueprint for the api
example_bp = Blueprint("example", __name__, url_prefix="/api/example")


@example_bp.get("/")  # this route would be .../api/example/
def exampleFunc():
    return jsonify({"exampleData": "test_success"})
