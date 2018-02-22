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

@application.route("/api/features", endpoint="api_features")
def api_features():
    if g.user is None:
        abort(404)

    x = int(request.args.get("x", -1))
    y = int(request.args.get("y", -1))
    if x < 0 and y < 0:
        abort(404)
    
    if CURRENT_MODEL != MODEL_LOGISITIC_REGRESSION:
        abort(404)
    
    feature_saved_data = JSONObjectData.last(JSONObjectData.FEATURE_TYPE_ID)
    if feature_saved_data is None:
        return None

    feature_maker   = SiteCommentFeatures.restore(json.loads(feature_saved_data.object_json), True)
    rude_comments   = SiteComment.rude_comments() 
    normal_comments = SiteComment.normal_comments()

    def get_data(feature_maker, comments, label):
        data = list()
        for comment in comments:
            feature = feature_maker.feature(comment)
            data.append({
                "x": feature_maker.manual_feature_value(feature, x),
                "y": feature_maker.manual_feature_value(feature, y),
                "label": label
            })
        return data

    positive_data = get_data(feature_maker, rude_comments, SiteCommentFeatures.RUDE_CLASS)
    negative_data = get_data(feature_maker, normal_comments, SiteCommentFeatures.NORMAL_CLASS)
    
    return jsonify(**{
        "x_name": SiteCommentFeatures.feature_desc(x),
        "y_name": SiteCommentFeatures.feature_desc(y),
        "positive": positive_data,
        "negative": negative_data 
    })