# encoding:utf-8
import requests
import logging
from operator import itemgetter
import json
import urllib
import re
import numpy as np
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

from flask import Flask, jsonify, render_template, g, url_for, redirect, request, session, abort, make_response
from flask.ext.babel import gettext, ngettext
from sqlalchemy import and_, desc
from sqlalchemy.sql import func
from flask.ext.sqlalchemy import Pagination

from meta import app as application, db, db_session, engine


@application.route("/index.html", endpoint="index")
@application.route("/", endpoint="index")
def index():
    return render_template('index.html')
