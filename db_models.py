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

class CommentStaticData:
    TotalNumberOfComments = 1025111
    rude_word_list = ["жопа","тугадум","отмазка","недоумок","предьява","гандон","говно","студент-халявщик","вопрошайка","lmgtfy","пися","говнецо","ничерта","говкод","студентота","пзд","хамьё","балван","болван","никчёмность","хуй","утырок","мудаки","мудак","аморально","шлюшка","топлёсс","путин","сцук","флейм","мудак","пидор","быдло","поебать","рот","гавнокодер","неадекват","кармадрочерство","олигофрен","хер","ржунимаг","гомосечь","тормаз","ебал","отсос","петушок","кретин","обсёр","срань","слобоумие","шлюха","гопник","дерьмо","хуесос","говносайт","говнокодер","шиза","ебло","говноконтора","гандон","ахинея","пиздец","некроговнокод","нахуя","шизофреник","похер","хуесос","маргинал","жлобство","дурачок","фалос","глупышка","говнарь","клоун","порно","балабол","нахуй","пукан","шут","ахуенно","ебанько","дятел","ебеня","хуйня","похуй","хам","писюн","уебок","задрот","писька","блять","мразь","дегенерат","хуева","подонок","ахренеть","слабак","пидарас","гондон","дибилизм","проститутка","ебать","ололоша","девка","бомжара","кармадрочер","чмошник","фриланс-биржа","пизда","убожество","сраный","бездарь","безмозглый","тупизм","гугл","стыдно","стыд","лень","лентяй","за тебя","в гугл","херня","погуглить","гуглить", "гребанный","ебаный","тухлый","убогоий","пендосский","блядский","ебанутый","ахуенный","вонючий","рукожопый","ёбаный","ебучая","проебанный","уебаный","ебучий","бляццкий","ленивый","смыться","бухать","просирать","выебываться","сьебаться","срать","потешаться","пыжиться","трахать","быдлокодить","пиздеть","лизать","понтоваться","обосраться","хуярить","дрочить","выбесить","подрочить","отсосать","вздрочнуть","ебануть","стебаться","насосать","нассать","гавнокодить","помастурбировать","полизать","пиздить","ахринеть","обосрать"]

class SiteComment(db.Model):
    __tablename__ = 'site_comment'
    
    id          = Column(Integer, primary_key=True)
    comment_id  = Column(BigInteger)
    question_id = Column(BigInteger)
    answer_id   = Column(BigInteger)
    post_author_id  = Column(BigInteger)
    post_score  = Column(Integer)

    title       = Column(String)
    body        = Column(String)
    processed_body  = Column(String)
    creation_date   = Column(DateTime, default=datetime.datetime.now)
    author_id   = Column(BigInteger)
    author_name = Column(String)
    diff_with_post= Column(BigInteger)

    is_verified = Column(Boolean, default=False)
    is_rude     = Column(Boolean, default=False)
    verified_user_id= Column(BigInteger)

    added       = Column(DateTime, default=datetime.datetime.now)
    analysed    = Column(DateTime)
    looks_rude  = Column(Boolean, default=False)

    def __init__(self, params):
        self.comment_id = params.get('comment_id')
        self.question_id= params.get('question_id')
        self.answer_id  = params.get('answer_id')
        self.post_author_id = params.get('post_author_id')
        self.post_score = params.get('post_score')
        self.diff_with_post = params.get('diff_with_post', 0)

        self.title      = params.get('title', "")
        self.body       = params.get('body')
        self.processed_body = params.get('processed_body')
        self.creation_date  = params.get('creation_date')
        self.author_id  = params.get('author_id')
        self.author_name= params.get('author_name')

        self.is_verified= params.get('is_verified', False)
        self.is_rude    = params.get('is_rude', False)
        self.verified_user = params.get('verified_user', -1)
        

        self.added      = datetime.datetime.now()
        self.analysed   = None
        self.looks_rude = False

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
        query = session.query(SiteComment).filter_by(is_rude=True).filter_by(is_verified=True).order_by(desc(SiteComment.creation_date))
        result = query.all()
        session.close()
        return result    

    @staticmethod
    def normal_comments():  
        session = db_session()
        query = session.query(SiteComment).filter_by(is_rude=False).filter_by(is_verified=True).order_by(desc(SiteComment.creation_date))
        result = query.all()
        session.close()
        return result    

    @staticmethod
    def unverified_comments():
        session = db_session()
        query = session.query(SiteComment).filter_by(is_verified=False).order_by(desc(SiteComment.creation_date))
        result = query.all()
        session.close()
        return result    

    @staticmethod
    def to_verify(start=0, limit=30):
        session = db_session()
        query = session.query(SiteComment).filter_by(is_verified=False).filter_by(looks_rude=True).order_by(desc(SiteComment.creation_date)).limit(limit)
        result = query.all()
        session.close()
        return result    