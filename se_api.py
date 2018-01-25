# encoding:utf-8
import requests
import logging
import json
import urllib
import re
import datetime
import time

from meta import STACKEXCHANGE_CLIENT_SECRET, STACKEXCHANGE_CLIENT_ID, STACKEXCHANGE_CLIENT_KEY


STACKEXCHANGE_COMMENT_ENDPOINT = "https://api.stackexchange.com/2.2/comments"
STACKEXCHANGE_COMMENT_ENDPOINT_FILTER = "!9Z(-x.SsB"
STACKEXCHANGE_ENDPOINT_SITE = "ru.stackoverflow"

def get_recent_comments(since_date):
    url = STACKEXCHANGE_COMMENT_ENDPOINT
    current_page = 1
    has_more = True
    comments = list()

    while has_more:
        params = {
            "key": STACKEXCHANGE_CLIENT_KEY,
            "site": STACKEXCHANGE_ENDPOINT_SITE,
            "order": "desc",
            "sort": "creation",
            "page": current_page,
            "fromdate": int(time.mktime(since_date.timetuple())),
            "filter": STACKEXCHANGE_COMMENT_ENDPOINT_FILTER
        }
        r = requests.get(url, data=params) 
        try: 
            data = json.loads(r.text)
        except:
            print(r.text)
            return comments

        error_id = int(data.get("error_id", 0))
        if error_id in [400]:
            print (data)
            return comments

        if data.get("items", None) is None:
            return comments

        for item in data["items"]:
            if item.get("owner", None) is not None:
                author_id = int(item["owner"]["user_id"])
            if item.get("creation_date", None) is not None:
                creation_date = datetime.datetime.utcfromtimestamp(
                    int(item["creation_date"])
                ).strftime('%Y-%m-%d %H:%M:%S')
            if item.get("post_id", None) is not None:
                post_id = int(item["post_id"])
            if item.get("comment_id", None) is not None:
                comment_id = int(item["comment_id"])
            if item.get("body", None) is not None:
                body = item["body"]
            
            comments.append((comment_id, post_id, body, creation_date, author_id))

        has_more = bool(data['has_more']) if data.get("has_more", None) is not None else False    
        current_page += 1

    return comments


  