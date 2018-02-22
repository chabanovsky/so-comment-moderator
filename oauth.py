import urllib
import logging
import requests
import json

from flask import Flask, jsonify, render_template, g, url_for, redirect, request, session

from meta import app as application, db_session, db, APP_URL
from db_models import User, DBModelAdder
from meta import STACKEXCHANGE_CLIENT_SECRET, STACKEXCHANGE_CLIENT_ID, STACKEXCHANGE_CLIENT_KEY

STACKEXCHANGE_OAUTH_ENDPOINT = "https://stackexchange.com/oauth"
STACKEXCHANGE_OAUTH_GET_ACCESS_TOKEN = "https://stackexchange.com/oauth/access_token"
STACKEXCHANGE_OAUTH_ME_ENDPOINT = "https://api.stackexchange.com/2.2/me"

def get_redirect_url():
    return APP_URL + url_for("stackexcange_oauth_callback")

@application.route("/oauth/logout")
@application.route("/oauth/logout/")
def logout_oauth():
    session.pop('account_id', None)
    return redirect(url_for("index"))
    
@application.route("/oauth/start")
@application.route("/oauth/start/")
def start_oauth():
    params = {
        "client_id": STACKEXCHANGE_CLIENT_ID,
        "scope": 'no_expiry', #"write_access,no_expiry",
        "redirect_uri": get_redirect_url()
    }
    url = STACKEXCHANGE_OAUTH_ENDPOINT + "?" + urllib.urlencode(params)
    return redirect(url)
    
@application.route("/oauth/stackexchange")
@application.route("/oauth/stackexchange/")
def stackexcange_oauth_callback():
    params = {
        "client_id": STACKEXCHANGE_CLIENT_ID,
        "client_secret": STACKEXCHANGE_CLIENT_SECRET,
        "code": request.args.get('code'),
        "redirect_uri": get_redirect_url()
    }    

    headers = {'content-type': "application/x-www-form-urlencoded"}

    r = requests.post(STACKEXCHANGE_OAUTH_GET_ACCESS_TOKEN, data=params, headers=headers)

    if r.status_code == 400:
        logging.error("Cannot authorise a user on SE OAuth. ")
        return redirect(url_for("index"))
    
    answers = r.text.split("&")
    token = ""
    for answer in answers:
        if "access_token" in answer:
            token = answer.split("=")[1]
            break

    if token == "":
        logging.error("Cannot obtain access token on SE OAuth.")
        return redirect(url_for("index"))
    
    session['access_token'] = token
    return redirect(url_for("login_oauth"))
    
@application.route("/oauth/login")    
@application.route("/oauth/login/")    
def login_oauth():
    if "access_token" not in session:
        return redirect(url_for("index"))

    params = {
        "site": "ru.stackoverflow",
        "order": "desc",
        "sort": "reputation",
        "key": STACKEXCHANGE_CLIENT_KEY, 
        "access_token": session['access_token']
    }

    r = requests.get(STACKEXCHANGE_OAUTH_ME_ENDPOINT, data=params)
    data = json.loads(r.text)
    account_id = -1
    user_id = -1
    display_name = ""
    role = ""
    reputation = -1
    profile_image = ""
    link = ""
    if data.get("items", None) is not None:
        for item in data["items"]:
            if item.get("account_id", None) is not None:
                account_id = item["account_id"]
            if item.get("user_id", None) is not None:
                user_id = item["user_id"]
            if item.get("display_name", None) is not None:    
                display_name = item["display_name"]
            if item.get("user_type", None) is not None:    
                role = item["user_type"]
            if item.get("reputation", None) is not None:    
                reputation = item["reputation"]
            if item.get("profile_image", None) is not None:    
                profile_image = item["profile_image"]
            if item.get("link", None) is not None:    
                link = item["link"]
    
    if account_id < 0 or user_id < 0 or display_name == "":
        logging.error("OAuth response: %s. Url: %s" % (r.text, r.url))
        logging.error("account_id: %s, user_id: %s, display_name: %s" % (str(account_id), str(user_id), display_name))
        return redirect(url_for("no_way"))

    adder = DBModelAdder()
    adder.start()
    user = User.get_by_account_id(account_id)
    if user is None:
        adder.add(User(account_id, 
            user_id, 
            display_name, 
            reputation, 
            profile_image,
            link,
            role))
    else:
        if user.username != display_name:
            user.username = display_name
        if user.role != role:
            user.role = role
        if user.reputation != reputation:
            user.reputation = reputation
        if user.profile_image != profile_image:
            user.profile_image = profile_image
        if user.profile_link != link:
            user.profile_link = link
        adder.add(user)
    adder.done()

    session["account_id"] = account_id
    return redirect(url_for("index"))