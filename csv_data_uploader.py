# encoding:utf-8
import csv
import collections
from datetime import datetime
import logging
import json

from db_models import DBModelAdder, SiteComment
from utils import process_text

VERIFIED_USER_ID_BY_DEFAULT = 6 # Let's say it's me.

class CSVDataUploader:
    
    def __init__(self, prefix="data/"):
        self.prefix = prefix

    def cvs_to_db(self):
        adder = DBModelAdder()
        adder.start()

        def add_to_db(adder, comments, verified, verified_user_id, is_rude):
            for parsed_args in comments:
                params = CSVDataUploader.make_site_comment_params(parsed_args, verified, verified_user_id, is_rude)
                if SiteComment.is_exist(adder, params.get('comment_id')):
                    continue
                adder.add(SiteComment(params))

        rude_cmnts = self.read_comments('rude_comments.csv')
        add_to_db(adder, rude_cmnts, datetime.now(), VERIFIED_USER_ID_BY_DEFAULT, True)

        normal_cmnts = self.read_comments('normal_comments.csv')
        add_to_db(adder, normal_cmnts, datetime.now(), VERIFIED_USER_ID_BY_DEFAULT, False)

        adder.done()

    def from_dump(self):
        adder = DBModelAdder()
        adder.start()

        def add(adder, comments):
            for comment in comments:
                if SiteComment.is_exist(adder, comment.get("comment_id")):
                    continue
                adder.add(SiteComment(comment))

        rude_comments = self.read_dumped_comments("rude_comments.csv")
        add(adder, rude_comments)
        normal_comments = self.read_dumped_comments("normal_comments.csv")
        add(adder, normal_comments)
        skipped_comments = self.read_dumped_comments("skipped_comments.csv")
        add(adder, skipped_comments)        

        adder.done()

    @staticmethod
    def make_site_comment_params(parsed_args, verified, verified_user_id, is_rude):
        comment_id, body, post_id, post_title, score, parent_post_id, creation_date, author_id, author_username, post_author_id, diff_with_post = parsed_args
        question_id = -1
        answer_id = -1
        if parent_post_id > 0:
            question_id = parent_post_id
            answer_id = post_id
        else:
            question_id = post_id

        return {
            'comment_id': comment_id,
            'question_id': question_id,
            'answer_id': answer_id,
            'post_author_id': post_author_id,
            'post_score': score,
            'body': body,
            'title': post_title,
            'processed_body': process_text(body),
            'creation_date': creation_date,
            'author_id': author_id,
            'author_name': author_username,
            'verified': verified,
            'verified_user_id': verified_user_id,
            'is_rude': is_rude,
            'diff_with_post': diff_with_post
        }
        

    def read_comments(self, filename='comments.csv'):
        pure_data = list()
        with open(self.prefix + filename, 'rt', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                # CommentId, c.Text, c.PostId, p.Score, p.ParentId, CommentCreationDate, CommentAuthorId, CommentAuthorUsername, PostAuthorId, DiffOfPost
                comment_id, body, post_link, score, parent_post_id, creation_date, author_id, author_username, post_author_id, diff_with_post = row
                try:
                    comment_id = int(comment_id)
                    score = int(score)
                    parent_post_id = -1 if parent_post_id is None or str(parent_post_id) == "" else int(parent_post_id)
                    creation_date = datetime.strptime(creation_date, "%Y-%m-%d %H:%M:%S")
                    author_id = int(author_id)
                    post_author_id = int(post_author_id)
                    diff_with_post = int(diff_with_post)
                    
                    data = json.loads(post_link)
                    if type(data) is int:
                        post_id = data    
                        post_title = ""
                    else:
                        post_id = int(data.get('id'))
                        post_title = data.get('title')
                except ValueError:
                    continue

                pure_data.append((comment_id, body, post_id, post_title, score, parent_post_id, creation_date, author_id, author_username, post_author_id, diff_with_post))

        return pure_data        

    def read_dumped_comments(self, filename='comments.csv'):
        data = list()
        def to_bool(field):
            return (str(field).lower() == 'true')

        def to_int(field, default_value=-1):
            try: 
                value = int(field)
                return value
            except ValueError:
                return default_value

        def to_date(field, default_value=None):
            date_format = "%Y-%m-%d %H:%M:%S"
            try: 
                value = datetime.strptime(field, date_format),
                return value
            except ValueError:
                return default_value
        
        with open(self.prefix + filename, 'rt', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                comment_id, question_id, answer_id, post_author_id, post_score, title, body, creation_date, author_id, author_name, diff_with_post, verified, is_rude, verified_user_id, added, analysed, looks_rude, skipped = row

                data_item = {
                    "comment_id": int(comment_id),
                    "question_id": int(question_id),
                    "answer_id": int(answer_id),
                    "post_author_id": int(post_author_id),
                    "post_score": int(post_score),
                    "title": title,
                    "body" : body,
                    "processed_body": process_text(body),
                    "creation_date": to_date(creation_date),
                    "author_id": int(author_id),
                    "author_name": author_name,
                    "diff_with_post": int(diff_with_post),
                    "verified": to_date(verified),
                    "is_rude": to_bool(is_rude),
                    "verified_user_id": to_int(verified_user_id),
                    "added": to_date(added),
                    "analysed": to_date(analysed),
                    "looks_rude": to_bool(looks_rude),
                    "skipped": to_date(skipped)
                }
                data.append(data_item)
        
        return data

            