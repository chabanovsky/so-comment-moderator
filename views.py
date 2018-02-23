# encoding:utf-8
import requests
import logging
from operator import itemgetter
import json
import urllib
import re
import numpy as np
import datetime
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

from flask import Flask, jsonify, render_template, g, url_for, redirect, request, session, abort, make_response
from flask.ext.babel import gettext, ngettext
from sqlalchemy import and_, desc
from sqlalchemy.sql import func
from flask.ext.sqlalchemy import Pagination

from meta import app as application, db, db_session, engine, FEED_APP_TITLE, APP_URL, SO_URL, clear_after_resp

from db_models import SiteComment, User
from api import *
from oauth import *

@application.before_request
def before_request():
    g.user = None
    if 'account_id' in session:
        g.user = User.get_by_account_id(int(session['account_id']))
        
@application.after_request
def after_request(response):
    clear_after_resp()
    return response    

@application.route("/", endpoint="index")
@application.route("/index", endpoint="index")
@application.route("/index.html", endpoint="index")
def index():
    return render_template('index.html', active_tab="index")  

@application.route("/comments", endpoint="comments")
@application.route("/comments/", endpoint="comments")
def comments():
    return redirect(url_for('comment_feed'))

@application.route("/comments/feed", endpoint="comment_feed")
@application.route("/comments/feed/", endpoint="comment_feed")
def comment_feed():
    limit = min(int(session.get("limit", 30)), 1000)
    comments = SiteComment.analysed_as_rude(limit)
    last_update = datetime.datetime.now()
    if len(comments) > 0:
        last_update = comments[0].analysed
    resp = make_response(render_template('feed_proto.xml', app_url=APP_URL, app_title=FEED_APP_TITLE, so_url=SO_URL, last_update=last_update, entries=comments))
    resp.headers['Content-type'] = 'application/atom+xml; charset=utf-8'
    return resp

@application.route("/features", endpoint="features")
@application.route("/features/", endpoint="features")
def features():
    if g.user is None:
        return redirect(url_for('index'))  
    return render_template('index.html', active_tab="features")

@application.route("/verifying", endpoint="verifying")
@application.route("/verifying/", endpoint="verifying")
def verifying():
    if g.user is None or g.user.role != "moderator":
        return redirect(url_for('index'))  
    page = max(int(request.args.get("page", 1)), 1)
    paginator = SiteComment.paginate_unverified(page)
    return render_template('index.html', paginator=paginator, base_url=url_for("verifying"), so_url=SO_URL, active_tab="verifying")

@application.route("/verified", endpoint="verified")
@application.route("/verified/", endpoint="verified")
def verified():
    if g.user is None or g.user.role != "moderator":
        return redirect(url_for('index'))  
    page = max(int(request.args.get("page", 1)), 1)
    paginator = SiteComment.paginate_verified(page)
    return render_template('index.html', paginator=paginator, base_url=url_for("verified"), so_url=SO_URL, active_tab="verified")

@application.route("/skipped", endpoint="skipped")
@application.route("/skipped/", endpoint="skipped")
def skipped():
    if g.user is None or g.user.role != "moderator":
        return redirect(url_for('index'))  
    page = max(int(request.args.get("page", 1)), 1)
    paginator = SiteComment.paginate_skipped(page)
    return render_template('index.html', paginator=paginator, base_url=url_for("skipped"), so_url=SO_URL, active_tab="skipped")

@application.route("/actions/actions_verify/<comment_id>", endpoint="actions_verify")
@application.route("/actions/actions_verify/<comment_id>/", endpoint="actions_verify")
def actions_verify(comment_id):
    if g.user is None or g.user.role != "moderator":
        abort(404)

    if request.args.get("is_rude", None) is None:
        abort(404)

    is_rude = json.loads(request.args.get("is_rude").lower())

    comment = SiteComment.by_comment_id(comment_id)
    if comment is None:
        abort(404)
    
    adder = DBModelAdder()
    adder.start()

    comment.verified = datetime.datetime.now()
    comment.is_rude = is_rude
    comment.verified_user_id = g.user.user_id
    comment.skipped = None

    adder.add(comment)
    adder.done()

    resp = {
        "status": True,
        "msg": "OK",
        "comment_id": comment_id,
        "is_rude": is_rude,
        "verified_user_id": g.user.user_id
    }    

    return jsonify(**resp)

@application.route("/actions/actions_skipp/<comment_id>", endpoint="actions_skipp")
@application.route("/actions/actions_skipp/<comment_id>/", endpoint="actions_skipp")
def actions_skipp(comment_id):
    if g.user is None or g.user.role != "moderator":
        abort(404)

    comment = SiteComment.by_comment_id(comment_id)
    if comment is None:
        abort(404)

    adder = DBModelAdder()
    adder.start()

    comment.skipped = datetime.datetime.now()
    comment.verified = None
    comment.verified_user = -1

    adder.add(comment)
    adder.done()

    resp = {
        "status": True,
        "msg": "OK",
        "comment_id": comment_id
    }    

    return jsonify(**resp)
        