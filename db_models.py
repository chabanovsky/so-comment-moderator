import datetime
import collections
import numpy as np
import csv

import logging

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean, ForeignKey, ColumnDefault, Float
from sqlalchemy import and_, or_, desc, asc, bindparam, text, Interval
from sqlalchemy.sql import func, select, update, literal_column, column, join
from sqlalchemy.dialects.postgresql import aggregate_order_by

from meta import app as application, db, db_session

class DBModelAdder:

    def __init__(self):
        self.session = None

    def start(self):
        self.session = db_session()

    def done(self):
        self.session.commit()
        self.session.close()  

    def execute(self, stmnt):
        self.session.execute(stmnt)

    def add(self, inst):
        self.session.add(inst)  

class SiteComment(db.Model):
    __tablename__ = 'site_comment'
    TotalNumberOfComments = 1025111

    id          = Column(Integer, primary_key=True)
    comment_id  = Column(BigInteger)
    post_id     = Column(BigInteger)
    body        = Column(String)
    processed_body  = Column(String)
    creation_date   = Column(DateTime, default=datetime.datetime.now)
    is_verified = Column(Boolean, default=False)
    is_rude     = Column(Boolean, default=False)
    author_id   = Column(BigInteger)
    verified_user   = Column(BigInteger)

    def __init__(self, comment_id, 
                post_id,
                body, 
                processed_body, 
                creation_date, 
                is_verified, 
                is_rude, 
                author_id,
                verified_user=-1):
        self.comment_id = comment_id
        self.post_id = post_id
        self.body   = body
        self.processed_body = processed_body
        self.creation_date = creation_date
        self.is_verified = is_verified
        self.is_rude = is_rude
        self.author_id = author_id
        self.verified_user = verified_user


    def __repr__(self):
        return '<%s %r>' % (SiteComment.__tablename__, str(self.id))

    @staticmethod
    def last_comment():
        session = db_session()
        query = session.query(SiteComment).order_by(desc(SiteComment.creation_date))
        result = query.first()
        session.close()
        return result

    @staticmethod
    def is_exist(adder, comment_id):
        return True if adder.session.query(func.count(SiteComment.id)).filter_by(comment_id=comment_id).scalar() > 0 else False

    @staticmethod
    def rude_comments():
        session = db_session()
        query = session.query(SiteComment).order_by(desc(SiteComment.creation_date)).filter_by(is_rude=True).filter_by(is_verified=True)
        result = query.all()
        session.close()
        return result    

    @staticmethod
    def normal_comments():  
        session = db_session()
        query = session.query(SiteComment).order_by(desc(SiteComment.creation_date)).filter_by(is_rude=False).filter_by(is_verified=True)
        result = query.all()
        session.close()
        return result    

    @staticmethod
    def unverified_comments():
        session = db_session()
        query = session.query(SiteComment).order_by(desc(SiteComment.creation_date)).filter_by(is_verified=False)
        result = query.all()
        session.close()
        return result    