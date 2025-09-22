import os

from flasgger import Swagger
from flask import Flask
from instagram.route import init_routes

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}
swagger = Swagger(app, config=swagger_config)


@app.route("/health", methods=["GET"])
def health_check():
    return "success", 200


init_routes(app)

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
