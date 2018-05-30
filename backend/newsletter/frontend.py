from flask import Blueprint


newsletter_frontend_blueprint = Blueprint(
    "newsletter_frontend", __name__, url_prefix="/newsletter")


@newsletter_frontend_blueprint.route("/")
def index():
    return "Vue.js"
