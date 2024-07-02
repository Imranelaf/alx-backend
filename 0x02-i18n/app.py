#!/usr/bin/env python3

'''
This module creates a Flask app.
'''

from flask_babel import Babel
import pytz
from flask import Flask, render_template, request, g



class Config(object):
    '''
    This class creates a configuration object.
    '''

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.timezoneselector
def get_timezone() -> str:
    '''
    This function determines the timezone.
    '''
    try:
        if request.args.get("timezone"):
            return pytz.timezone(request.args.get("timezone")).zone
        if g.user and g.user.get("timezone"):
            return pytz.timezone(g.user["timezone"]).zone
    except pytz.exceptions.UnknownTimeZoneError:
        pass
    return "UTC"


def get_user() -> dict:
    '''
    This function returns a user dictionary or None if the ID cannot be
    found or if login_as was not passed.
    '''
    usrid = request.args.get("login_as")
    if usrid and int(usrid) in users:
        return users[int(usrid)]
    return None


@app.before_request
def before_request() -> None:
    '''
    This function sets the user before the request.
    '''
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    '''
    This function determines the best match with our supported languages.
    '''
    if request.args.get("locale") in app.config["LANGUAGES"]:
        return request.args.get("locale")
    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user["locale"]
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    '''
    This function returns a string.
    '''
    from flask_babel import format_datetime
    from datetime import datetime

    curr_time = format_datetime(datetime.utcnow())
    return render_template("index.html", current_time=curr_time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
