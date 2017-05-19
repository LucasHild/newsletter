# newsletter
Newsletter system for my blog

### [newsletter.py](https://github.com/Lanseuo/newsletter/blob/master/newsletter.py)

API handling GET and POST requests

The API is written in [Flask](http://flask.pocoo.org/). There are several API endpoints for subscribing and unsubscribing to the newsletter. The data is stored in a MongoDB-Database

### [send_newsletter.py](https://github.com/Lanseuo/newsletter/blob/master/send_newsletter.py)

Sending issues

You specify the html template and the mail will be send to all users from db.

### [template.html](https://github.com/Lanseuo/newsletter/blob/master/template.html)

Mail template
