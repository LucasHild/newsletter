import config
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
import pymongo
from pymongo import MongoClient

def get_users():
    uri = "mongodb://" + config.mongodb_username + ":" + config.mongodb_password + "@" + config.mongodb_host + ":" + config.mongodb_port + "/" + config.mongodb_db
    client = MongoClient(uri)
    db = client.newsletter
    users = db.users
    userList = [user for user in users.find()]
    return userList

def get_file(filename):
    with open(filename, "r") as f:
        content = f.read()
        f.close()
    return content

def sendTestMail():
    """Test it by sending mail to me"""
    user_mail = config.mail_test
    msg = MIMEMultipart('alternative')
    msg['To'] = email.utils.formataddr(('You', user_mail))
    msg['From'] = email.utils.formataddr(('Lucas Hild', config.mail_sender))
    msg['Subject'] = 'TEST: Lucas Hild - Newsletter'
    html = get_file(file)
    msg.attach(MIMEText(html, 'html'))

    smtpserver = config.mail_server
    smtpuser = config.mail_sender
    smtppass = config.mail_password

    receivers = [user_mail]
    sender = config.mail_sender

    session = smtplib.SMTP(smtpserver, port=587)
    session.login(smtpuser, smtppass)
    session.sendmail(smtpuser, user_mail, msg.as_string())
    print("Sent Message to: " + user_mail)

    print("Type: 'yes it worked'")
    confirm = str()
    while confirm != "yes it worked":
        confirm = input("Check: ")

def sendMail(mail):
    msg = MIMEMultipart('alternative')
    msg['To'] = email.utils.formataddr(('You', mail))
    msg['From'] = email.utils.formataddr(('Lucas Hild', config.mail_sender))
    msg['Subject'] = 'Lucas Hild - Newsletter'
    html = get_file(file)
    msg.attach(MIMEText(html, 'html'))

    smtpserver = config.mail_server
    smtpuser = config.mail_sender
    smtppass = config.mail_password

    receivers = [mail]
    sender = config.mail_sender

    session = smtplib.SMTP(smtpserver, port=587)
    session.login(smtpuser, smtppass)
    session.sendmail(smtpuser, mail, msg.as_string())
    print("Sent Message to: " + mail)
    sleep(1)

file = input("File: ")
# TODO: Check file

sendTestMail()

# Send mail to every user
users = get_users()
for user in users:
    user_mail = user["mail"]
    sendMail(user_mail)
