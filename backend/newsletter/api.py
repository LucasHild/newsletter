import requests
from flask import Blueprint, jsonify, request

import config
import authentication
from .generate import generate_html, generate_plain


mailerlite_base_url = "https://api.mailerlite.com/api/v2/"
headers = {
    "X-MailerLite-ApiKey": config.mailerlite_api_key
}

newsletter_api_blueprint = Blueprint(
    "newsletter_api", __name__, url_prefix="/api/newsletter")


@newsletter_api_blueprint.route("/upload", methods=["POST"])
@authentication.login_required
def upload():
    if not request.json.get("campaign_id"):
        r = requests.post(
            f"{mailerlite_base_url}campaigns",
            json={
                "type": "regular",
                "subject": request.json.get("subject"),
                "language": "de",
                "groups": [config.mailerlite_newsletter_group]
            },
            headers=headers)

        if r.status_code != 200:
            return jsonify({"error": r.json()["error"]["message"]}), 500

        campaign_id = r.json()["id"]
        mail_id = r.json()["mail_id"]
    else:
        campaign_id = request.json.get("campaign_id")
        mail_id = request.json.get("mail_id")

    r = requests.put(
        f"{mailerlite_base_url}campaigns/{campaign_id}/content",
        json={
            "auto_inline": True,
            "html": generate_html(
                request.json.get("introduction"),
                request.json.get("blogArticles"),
                request.json.get("topArticles")
            ),
            "plain": generate_plain(
                request.json.get("introduction"),
                request.json.get("blogArticles"),
                request.json.get("topArticles")
            )
        },
        headers=headers
    )

    if r.status_code != 200:
        return jsonify({"error": r.json()["error"]["message"]}), 500

    return jsonify({
        "campaign_id": campaign_id,
        "mail_id": mail_id
    })


@newsletter_api_blueprint.route("/send", methods=["POST"])
@authentication.login_required
def send():
    campaign_id = request.json.get("campaignId")
    r = requests.post(
        f"{mailerlite_base_url}campaigns/{campaign_id}/actions/send",
        headers=headers
    )

    print(r.json())

    if r.status_code != 200:
        return jsonify({"error": r.json()["error"]["message"]}), 500

    return jsonify({"success": True})
