# encoding:utf-8
import requests
import logging
import json
import urllib
import re
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

from flask import Flask, jsonify, render_template, g, url_for, redirect, request, session, abort, make_response

from meta import app as application

@application.route("/api/features", endpoint="api_features")
def api_features():
    feature = int(session.get("feature", 0))
    return jsonify(**{})