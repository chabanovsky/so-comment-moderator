# encoding:utf-8
import csv
import collections
from datetime import datetime
import logging

from db_models import DBModelAdder, SiteComment
from utils import process_text

VERIFIED_USER_ID_BY_DEFAULT = 6 # Let's say it's me.

class CSVDataUploader:
    
    def __init__(self, prefix="data/"):
        self.prefix = prefix

    def cvs_to_db(self):
        adder = DBModelAdder()
        adder.start()

        rude_cmnts = self.read_comments('rude_comments.csv')
        for comment_id, body, post_id, creation_date, author_id in rude_cmnts:
            if SiteComment.is_exist(adder, comment_id):
                continue

            adder.add(
                SiteComment(comment_id, 
                            post_id, 
                            body, 
                            process_text(body), 
                            creation_date, 
                            True, True, 
                            author_id, 
                            VERIFIED_USER_ID_BY_DEFAULT)
                )

        normal_cmnts = self.read_comments('normal_comments.csv')
        for comment_id, body, post_id, creation_date, author_id in normal_cmnts:
            if SiteComment.is_exist(adder, comment_id):
                continue

            adder.add(
                SiteComment(comment_id, 
                            post_id, 
                            body, 
                            process_text(body), 
                            creation_date, 
                            True, False, 
                            author_id, 
                            VERIFIED_USER_ID_BY_DEFAULT)
                )


        adder.done()

    def read_comments(self, filename='comments.csv'):
        pure_data = list()
        with open(self.prefix + filename, 'rt', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                comment_id, body, post_id, creation_date, author_id = row
                try:
                    comment_id = int(comment_id)
                    post_id = int(post_id)
                    author_id = int(author_id)
                    creation_date = datetime.strptime(creation_date, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

                pure_data.append((comment_id, body, post_id, creation_date, author_id))

        return pure_data        