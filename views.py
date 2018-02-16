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

from meta import app as application, db, db_session, engine, FEED_APP_TITLE, APP_URL, SO_URL

from db_models import SiteComment

@application.route("/", endpoint="index")
@application.route("/index", endpoint="index")
@application.route("/index.html", endpoint="index")
def index():
    return redirect(url_for('comment_feed'))  

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
    resp = make_response(render_template('feed_proto.xml', app_title=FEED_APP_TITLE, so_url=SO_URL, last_update=last_update, entries=comments))
    resp.headers['Content-type'] = 'text/xml; charset=utf-8'
    return resp

@application.route("/features", endpoint="features")
@application.route("/features/", endpoint="features")
def features():
    return render_template('features.html')