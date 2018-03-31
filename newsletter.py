import config
import email.utils
import datetime
import random
import smtplib

from app import app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from inlinestyler.utils import inline_css
from flask import request, jsonify, session, redirect, url_for
from functools import wraps
from pymongo import MongoClient


def connection():
    """Connection to MongoDB database"""
    uri = "mongodb://" + config.mongodb_username + ":" + config.mongodb_password + \
        "@" + config.mongodb_host + ":" + config.mongodb_port + "/" + config.mongodb_db
    client = MongoClient(uri)
    db = client.newsletter
    return db, client


def login_required(f):
    """Decorator checks whether user is logged in"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session or request.form.get("password") == config.web_password:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("newsletter_login_get"))
    return wrap


@app.route("/newsletter/", methods=["GET", "POST"])
@login_required
def newsletter():
    """Write and edit newsletters"""
    return app.send_static_file("newsletter.html")


@app.route("/newsletter/login/", methods=["GET"])
def newsletter_login_get():
    """Login screen"""
    if "logged_in" in session:
        return redirect(url_for("newsletter"))

    return app.send_static_file("newsletter-login.html")


@app.route("/newsletter/login/", methods=["POST"])
def newsletter_login_post():
    """Checks login"""
    attempted_username = request.form["username"]
    attempted_password = request.form["password"]

    # Check whether password is correct
    if attempted_username == config.web_username and attempted_password == config.web_password:
        session["logged_in"] = True
        return redirect(url_for("newsletter"))
    else:
        return redirect(url_for("newsletter_login_get"))


@app.route("/newsletter/logout/")
def newsletter_logout():
    """User logs out"""
    # Clear session
    session.clear()
    return redirect(url_for("newsletter_login_get"))


@app.route("/newsletter/users/")
def newsletter_users():
    """Displays the users"""
    return app.send_static_file("newsletter-users.html")


@app.route("/newsletter/api/users/")
@login_required
def newsletter_api_users():
    """API for users"""
    db, client = connection()

    # Get list of users
    users = db.users
    user_list = [user for user in users.find()]

    # Create output
    result = list()
    for user in user_list:
        result.append({
            "mail": user["mail"],
            "state": user["state"],
            "registration_date": user["registration_date"],
            "source": user["source"]
        })

    return jsonify(result)


@app.route("/newsletter/api/send/", methods=["POST"])
@login_required
def newsletter_api_send_test():
    """API for sending a new issue"""
    # Get form data
    raw_html = request.form["html"]
    type = request.form["type"]  # 'test' or 'all'

    # Get css file
    with open("static/lucas-newsletter.css", "r") as f:
        css = f.read()

    # Generate and compile html
    html_external_css = "<html><head><meta charset='utf-8'><style>" + \
        css + "</style></head><body>" + raw_html + "</body></html>"
    html = inline_css(html_external_css)

    if type == "test":
        # Set mail configuration
        user_mail = config.mail_test
        msg = MIMEMultipart('alternative')
        msg['To'] = email.utils.formataddr(('You', user_mail))
        msg['From'] = email.utils.formataddr(('Lucas Hild', config.mail_sender))
        msg['Subject'] = 'TEST: Lucas Hild - Newsletter'
        msg.attach(MIMEText(html, 'html'))

        # Set mail server configuration
        smtpserver = config.mail_server
        smtpuser = config.mail_sender
        smtppass = config.mail_password

        # Send mail
        smtpsession = smtplib.SMTP(smtpserver, port=587)
        smtpsession.login(smtpuser, smtppass)
        smtpsession.sendmail(smtpuser, user_mail, msg.as_string())

        return jsonify({"success": "Sent mail"})

    elif type == "all":
        # Get list of users
        db, client = connection()
        users = [user for user in db.users.find() if user["state"] == "confirmed"]

        # For every user
        for user in users:
            # Set mail configuration
            user_mail = user["mail"]
            msg = MIMEMultipart('alternative')
            msg['To'] = email.utils.formataddr(('You', user_mail))
            msg['From'] = email.utils.formataddr(('Lucas Hild', config.mail_sender))
            msg['Subject'] = 'Lucas Hild - Newsletter'
            msg.attach(MIMEText(html, 'html'))

            # Set mail server configuration
            smtpserver = config.mail_server
            smtpuser = config.mail_sender
            smtppass = config.mail_password

            # Send mail
            smtpsession = smtplib.SMTP(smtpserver, port=587)
            smtpsession.login(smtpuser, smtppass)
            smtpsession.sendmail(smtpuser, user_mail, msg.as_string())
            print("Sent Message to: " + user_mail)

        return jsonify({"success": "Sent mail"})

    return jsonify({"error": "Sent no mail"})


@app.route("/newsletter/subscribe", methods=["GET", "POST"])
def newsletter_subscribe():
    """Subscribe to the newsletter"""
    db, client = connection()

    if request.method == "POST":
        # Get form data
        mail = request.form["mail"].strip()
        source = request.form["source"]

        # Check whether all arguments are given
        if not mail:
            return jsonify({"error": "Keine Mail-Adresse angegeben"})

        # Check whether all arguments are given
        if not "@" in mail or not "." in mail:
            return jsonify({"error": "Keine Mail-Adresse angegeben"})

        # Check whether mail is already in db
        if db.users.find_one({"mail": mail}):
            return jsonify({"error": "Du hast Dich schon für den Newsletter angemeldet"})

        # TODO: If user unsubscribed and wants to subscribe again

        # Generate confirmation code
        confirmation_code = str(random.randint(1000, 9999))

        try:
            user = {
                "mail": mail,
                "source": source,
                "registration_date": datetime.datetime.now().strftime("%y-%m-%d"),
                "state": confirmation_code
            }

            # Insert user to db
            db.users.insert_one(user)

        except:
            return jsonify({"error": "Ein Fehler ist aufgetreten! Versuche es später noch einmal!"})

        # Send confirmation mail
        # Set mail configuration
        msg = MIMEMultipart('alternative')
        msg['To'] = email.utils.formataddr(('You', mail))
        msg['From'] = email.utils.formataddr(('Lucas Hild', config.mail_sender))
        msg['Subject'] = 'Bestätige: Lucas Hild - Newsletter'

        # Get html file
        with open("confirm-newsletter.html", "r") as f:
            html = f.read()
            f.close()

        # Replace placholders
        html = html.replace("put_confirmation_code_here", confirmation_code, 1)
        html = html.replace("put_mail_here", mail, 1)

        msg.attach(MIMEText(html, 'html'))

        # Set mail server configuration
        smtpserver = config.mail_server
        smtpuser = config.mail_sender
        smtppass = config.mail_password

        # Send mail
        smtpsession = smtplib.SMTP(smtpserver, port=587)
        smtpsession.login(smtpuser, smtppass)
        smtpsession.sendmail(smtpuser, mail, msg.as_string())

        return jsonify({"success": "subscribed"})

    else:
        # Redirect to my website
        return "<meta http-equiv='refresh' content='0; url=https://lucas-hild.de/'/>"


@app.route("/newsletter/confirm")
def newsletter_confirm():
    """Confirm newsletter"""
    try:
        # Get form values
        confirmation_code = request.args.get('confirmation_code')
        mail = request.args.get("mail")
    except:
        html = """
        <meta http-equiv='refresh' content='3; url=https://lucas-hild.de/'/><h
        <h1 style='font-family: sans-serif'>Ein Fehler ist aufgetreten!</h1>
        <p style='font-family: sans-serif'>Der Bestätigungscode funktioniert nicht.</p>
        """
        return html

    # Get user from db
    db, client = connection()
    user = db.users.find_one({"mail": mail})

    # Check whether mail is valid
    if user:
        # Check whether confirmation code is valid
        if confirmation_code == user["state"]:
            db.users.update_one({"mail": mail},
                                {"$set": {"state": "confirmed"}})

            return "<h1 style='font-family: sans-serif'>Du hast den Newsletter erfolgreich abonniert!</h1>"
        else:
            html = """
            <meta http-equiv='refresh' content='3; url=https://lucas-hild.de/'/><h
            <h1 style='font-family: sans-serif'>Ein Fehler ist aufgetreten!</h1>
            <p style='font-family: sans-serif'>Der Bestätigungscode funktioniert nicht.</p>
            """
            return html
    else:
        html = """
        <meta http-equiv='refresh' content='3; url=https://lucas-hild.de/'/><h
        <h1 style='font-family: sans-serif'>Ein Fehler ist aufgetreten!</h1>
        <p style='font-family: sans-serif'>Der Bestätigungscode funktioniert nicht.</p>
        """
        return html


@app.route("/newsletter/unsubscribe", methods=["GET", "POST"])
def newsletter_unsubscribe():
    """Unsubscribe from newsletter"""
    if request.method == "GET":
        # Render unsubscribe form
        return """
        <h1 style='font-family: sans-serif'>Abmelden von Lucas Hild Newsletter</h1>
        <form action="" method="post">
            <input type="text" name="mail" placeholder="Deine Mail Adresse" required>
            <input type="submit" value="Abmelden">
        </form>
        """

    elif request.method == "POST":
        # Unsubscribe user

        # Get form values
        mail = request.form["mail"]

        db, client = connection()

        # If user is in database
        if db.users.find_one({"mail": mail}) != None:
            # Set state to unsubscribed
            db.users.update_one(
                {'mail': mail},
                {'$set': {"state": "unsubscribed"}}
            )
            return "<h1 style='font-family: sans-serif'>Schade! Du wirst in Zukunft keine Mails mehr von mir erhalten.</h1>"

        else:
            return "<h1 style='font-family: sans-serif'>Du warst nie für den Newsletter angemeldet!</h1>"
