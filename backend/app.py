from flask import Flask, jsonify
from flask_cors import CORS

import config
import authentication
import newsletter

app = Flask(__name__)
app.secret_key = config.secret_key
CORS(app)


@app.route("/")
def index():
    return jsonify({
        "message": "You're on the server"
    })

app.add_url_rule(
    "/api/login",
    "api-login",
    authentication.login,
    methods=["POST"]
)

app.register_blueprint(newsletter.newsletter_api_blueprint)
app.register_blueprint(newsletter.newsletter_frontend_blueprint)
