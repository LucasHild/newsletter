from app import app
from flask import request, jsonify

import config

import datetime

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
            <meta http-equiv='refresh' content='3; url=https://blog.lucas-hild.de/'/><h
            <h1 style='font-family: sans-serif'>Keine Mail Adresse angegeben</h1>
            <p style='font-family: sans-serif'>Du wirst weitergeleitet</p>
            """
            return html

        # TODO: Check whether mail is already in db

        try:
            user = {
                "mail": mail,
                "source": source,
                "registration_date": datetime.datetime.now().strftime("%y-%m-%d"),
                "state": "unconfirmed"
            }

            id = users.insert_one(user).inserted_id

            # TODO: Confirm subscription
        except:
            # Redirect to my blog
            return "<meta http-equiv='refresh' content='0; url=https://blog.lucas-hild.de/'/>"

        # Redirect to information page on my blog
        return "<meta http-equiv='refresh' content='0; url=https://blog.lucas-hild.de/newsletter-subscribe/'/>"

    else:
        # Redirect to my blog
        return "<meta http-equiv='refresh' content='0; url=https://blog.lucas-hild.de/'/>"


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