from app import app
from flask import request, jsonify

import config

import datetime
import random
import smtplib

import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


def connection():
    uri = "mongodb://" + config.mongodb_username + ":" + config.mongodb_password + "@" + config.mongodb_host + ":" + config.mongodb_port + "/" + config.mongodb_db
    client = MongoClient(uri)
    db = client.newsletter
    return db, client


@app.route("/newsletter")
def newsletter():
    try:
        password = request.args.get('password')
    except:
        password = str()

    if password == config.api_password:
        db, client = connection()
        users = db.users
        userList = [user for user in users.find()]

        # Create output
        jsonOutput = list()
        for user in userList:
            jsonOutput.append({
                "mail": user["mail"],
                "state": user["state"],
                "registration_date": user["registration_date"],
                "source": user["source"]
            })

        return jsonify(jsonOutput)
    else:
        return jsonify("Access denied!")


@app.route("/newsletter/subscribe", methods=["GET", "POST"])
def newsletterSubscribe():
    db, client = connection()
    users = db.users

    if request.method == "POST":
        mail = request.form["mail"]
        source = request.form["source"]

        # Check whether all arguments are given
        if not mail:
            html = """
            <meta http-equiv='refresh' content='3; url=https://blog.lucas-hild.de/'/><h
            <h1 style='font-family: sans-serif'>Keine Mail Adresse angegeben</h1>
            <p style='font-family: sans-serif'>Du wirst weitergeleitet</p>
            """
            return html

        # Check whether all arguments are given
        if not "@" in mail or not "." in mail:
            html = """
            <meta http-equiv='refresh' content='3; url=https://lucas-hild.de/'/><h
            <h1 style='font-family: sans-serif'>Keine Mail Adresse angegeben</h1>
            <p style='font-family: sans-serif'>Du wirst weitergeleitet</p>
            """
            return html

        # Check whether mail is already in db
        if db.users.find_one({"mail": mail}):
            html = """
                        <meta http-equiv='refresh' content='3; url=https://lucas-hild.de/'/><h
                        <h1 style='font-family: sans-serif'>Du hast Dich schon für den Newsletter angemeldet</h1>
                        <p style='font-family: sans-serif'>Du wirst weitergeleitet</p>
                        """
            return html

        # Generate confirmation code
        confirmation_code = str(random.randint(1000, 9999))

        try:
            user = {
                "mail": mail,
                "source": source,
                "registration_date": datetime.datetime.now().strftime("%y-%m-%d"),
                "state": confirmation_code
            }

            id = users.insert_one(user).inserted_id

        except:
            return """
            <meta http-equiv='refresh' content='2; url=https://lucas-hild.de/'/>
            <h1 style='font-family: sans-serif'>Ein Fehler ist aufgetreten! Versuche es später noch einmal!</h1>
            """

        # Send confirmation mail
        msg = MIMEMultipart('alternative')
        msg['To'] = email.utils.formataddr(('You', mail))
        msg['From'] = email.utils.formataddr(('Lucas Hild', config.mail_sender))
        msg['Subject'] = 'Bestätige: Lucas Hild - Newsletter'

        with open("confirm-newsletter.html", "r") as f:
            html = f.read()
            f.close()
        html = html.replace("put_confirmation_code_here", confirmation_code, 1)
        html = html.replace("put_mail_here", mail, 1)

        msg.attach(MIMEText(html, 'html'))

        smtpserver = config.mail_server
        smtpuser = config.mail_sender
        smtppass = config.mail_password

        receivers = [mail]
        sender = config.mail_sender

        session = smtplib.SMTP(smtpserver, port=587)
        session.login(smtpuser, smtppass)
        session.sendmail(smtpuser, mail, msg.as_string())

        # Check source and redirect back
        if source == "blog-footer":
            # Redirect to information page on my blog
            return "<meta http-equiv='refresh' content='0; url=https://blog.lucas-hild.de/newsletter-subscribe/'/>"
        else:
            # Redirect to page on my website
            return """
            <meta http-equiv='refresh' content='5; url=https://lucas-hild.de/'/>
            <h1 style='font-family: sans-serif'>Du wurdest erfolgreich zu meinem Newsletter angemeldet!</h1>
            <p style='font-family: sans-serif'>Nun musst Du nur noch auf den Link in deinen Mail klicken!</h1>
            """

    else:
        # Redirect to my blog
        return "<meta http-equiv='refresh' content='0; url=https://lucas-hild.de/'/>"


@app.route("/newsletter/confirm")
def newsletterConfirm():
    try:
        confirmation_code = request.args.get('confirmation_code')
        mail = request.args.get("mail")
    except:
        html = """
        <meta http-equiv='refresh' content='3; url=https://lucas-hild.de/'/><h
        <h1 style='font-family: sans-serif'>Ein Fehler ist aufgetreten!</h1>
        <p style='font-family: sans-serif'>Der Bestätigungscode funktioniert nicht.</p>
        """
        return html

    db, client = connection()

    user = db.users.find_one({"mail": mail})
    print(user)
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


@app.route("/newsletter/unsubscribe", methods=["GET", "POST"])
def newsletterUnsubscribe():
    if request.method == "GET":
        HTML = """
        <h1 style='font-family: sans-serif'>Abmelden von Lucas Hild Newsletter</h1>
        <form action="" method="post">
            <input type="text" name="mail" placeholder="Deine Mail Adresse" required>
            <input type="submit" value="Abmelden">
        </form>
        """
        return HTML

    elif request.method == "POST":
        mail = request.form["mail"]
        db, client = connection()
        users = db.users

        if users.find_one({"mail": mail}) != None:
            users.update_one(
                {'mail': mail},
                {'$set': {"state": "unsubscribed"}}
            )
            return "Schade! Du wirst in Zukunft keine Mails mehr von mir erhalten."

        else:
            return "Du warst nie für den Newsletter angemeldet!"