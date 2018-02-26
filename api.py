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

from meta import app as application, CURRENT_MODEL, MODEL_LOGISITIC_REGRESSION
from db_models import JSONObjectData, SiteComment
from features import SiteCommentFeatures
from wiktionary_org import WiktionaryOrg

@application.route("/api/features", endpoint="api_features")
@application.route("/api/features/", endpoint="api_features")
def api_features():
    if g.user is None:
        abort(404)

    x = int(request.args.get("x", -1))
    if x < 0:
        abort(404)
    
    if CURRENT_MODEL != MODEL_LOGISITIC_REGRESSION:
        abort(404)
    
    rude_comments   = SiteComment.rude_comments() 
    normal_comments = SiteComment.normal_comments()

    def get_data(comments, feature, label):
        data = list()
        for comment in comments:
            feature_value = SiteCommentFeatures.manual_feature_value(comment, feature)
            data.append({
                "x": feature_value,
                "label": label
            })
        return data

    positive_data = get_data(rude_comments, x, SiteCommentFeatures.RUDE_CLASS)
    negative_data = get_data(normal_comments, x, SiteCommentFeatures.NORMAL_CLASS)
    
    return jsonify(**{
        "x_name": SiteCommentFeatures.feature_desc(x),
        "positive": positive_data,
        "negative": negative_data 
    })

@application.route("/api/wiktionary-org", endpoint="api_wiktionary_org")
@application.route("/api/wiktionary-org/", endpoint="api_wiktionary_org")
def api_wiktionary_org():
    if g.user is None:
        abort(404)    

    words = int(request.args.get("words", None))
    if words is None:
        abort(404)

    data = WiktionaryOrg.get_props(words)()
    return jsonify(**{
        "items": data
    })
    
@application.route("/api/roc", endpoint="api_roc")
@application.route("/api/roc/", endpoint="api_roc")
def api_roc():
    if g.user is None:
        abort(404)
    
    if CURRENT_MODEL != MODEL_LOGISITIC_REGRESSION:
        abort(404)

    items = JSONObjectData.all_extra(JSONObjectData.LOGREG_TYPE_ID)
    objects = []
    for item in items:
        objects.append({
            "extra": item.extra,
            "added": item.added
        })
         
    return jsonify(**{
        "items": objects
    })