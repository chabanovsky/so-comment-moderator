# encoding:utf-8
import datetime
import collections
import csv

import logging

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean, ForeignKey, ColumnDefault, Float
from sqlalchemy import and_, or_, desc, asc, bindparam, text, Interval
from sqlalchemy.sql import func, select, update, literal_column, column, join
from sqlalchemy.dialects.postgresql import aggregate_order_by

from meta import app as application, db, db_session
from utils import process_text

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
    rude_word_list = ["жопа","тугадум","отмазка","недоумок","предьява","гандон","говно","студент-халявщик","вопрошайка","lmgtfy","пися","говнецо","ничерта","говкод","студентота","пзд","хамьё","балван","болван","никчёмность","хуй","утырок","мудаки","мудак","аморально","шлюшка","топлёсс","путин","сцук","флейм","мудак","пидор","быдло","поебать","рот","гавнокодер","неадекват","кармадрочерство","олигофрен","хер","ржунимаг","гомосечь","тормаз","ебал","отсос","петушок","кретин","обсёр","срань","слобоумие","шлюха","гопник","дерьмо","хуесос","говносайт","говнокодер","шиза","ебло","говноконтора","гандон","ахинея","пиздец","некроговнокод","нахуя","шизофреник","похер","хуесос","маргинал","жлобство","дурачок","фалос","глупышка","говнарь","клоун","порно","нахуй","пукан","шут","ахуенно","ебанько","дятел","ебеня","хуйня","похуй","хам","писюн","уебок","задрот","писька","блять","мразь","дегенерат","хуев","подонок","ахренеть","слабак","пидарас","гондон","дибилизм","проститутка","ебать","ололоша","девка","бомжара","кармадрочер","чмошник","фриланс-биржа","пизда","убожество","сраный","бездарь","безмозглый","тупизм","гугл","стыдно","стыд","лень","лентяй","за тебя","в гугл","херня","погуглить","гуглить", "гребанный","ебаный","тухлый","убогий","пендосский","блядский","ебанутый","ахуенный","вонючий","рукожопый","ёбаный","ебучая","проебанный","уебаный","ебучий","бляццкий","ленивый","смыться","бухать","просирать","выебываться","сьебаться","срать","потешаться","пыжиться","трахать","быдлокодить","пиздеть","лизать","понтоваться","обосраться","хуярить","дрочить","выбесить","подрочить","отсосать","вздрочнуть","ебануть","стебаться","насосать","нассать","гавнокодить","помастурбировать","полизать","пиздить","ахринеть","обосрать"]
    additional_stop_words = ['fuck', 'наркоман', 'женщина', 'бабло', 'холивар', 'кэп', 'говнокод', 'неадекватен', 'тролль', 'нахрена', 'хрен', 'бля', 'блядь', 'школоло', 'баттхерт', 'нах', 'телепат', 'экстрасенс', 'троллинг', 'умник', 'нихера', 'шняга', 'матчасть', 'впадлу', 'школьник', 'нуб', 'попец', 'хуле', 'з****ли', 'бл**', 'бл*ть', 'на***', 'г**о', 'пиз*ц', 'бл*', 'епта', 'ебн*тый', 'под***ать', 'п*зд*ц', 'поп*й', 'х***', 'дыбил', 'тупой', 'урод', 'телка', 'дурик', 'глупый', 'бред', 'балда', 'дичь', 'хреновина', '**ев', 'чушь', 'ноют', 'ныть', 'заебал', 'долбаеб', 'банальщина', 'дурак', 'обоснуй', 'нах*й', 'хамло', 'отстой', 'тварь', 'козел', 'чмо', 'пидарьё', 'wtf', 'г....о', 'аболтус', 'идиотский', 'идиот', 'чудик', 'хуясебе', 'балабол', 'сосать', 'дебил', 'соизвольте', 'вонючий', 'пзда', 'фуфло', 'грёбанный', 'колхозник', 'дерзить', 'убиться', 'бегом', 'херь', 'малолетка', 'бесполезный', 'кривой', 'дебильная', 'уебки', 'чувак', 'даун', 'очнись', 'дохрена', 'бредово', 'неадекватный', 'омг', 'бестолковый', 'мочер', 'дигенерат', 'некомпетентный', 'дятел', 'bullshit', 'петух', 'нытик', 'поржал', 'пох', 'обоссать', 'ху*ями', 'задница', 'олень', 'пиз*ц', 'чукча', 'тупанул', 'чувачок', 'глупость', 'хамье', 'еврей', 'вахтёр', 'вахтер', 'сиськи', 'шизик', 'аутист', 'бесить', 'отсоси', 'отсасывать', 'пудак', 'тугадум', 'ерунда', 'долдон', 'бляццкие', 'бляцкий', 'посмеялся', 'ересь', 'ерись', 'ебаньки', 'кармодрочер', 'погуглю', 'нубов', 'школа', 'жесть', 'уё*ки', 'ебеня', 'спам', 'минус', 'минусете', 'минусовать', 'ахереть']
    processed_rude_word_list = None
    serach_links = ['google.com', 'google.ru', 'google.com.ua', 'yandex.ua', 'lmgtfy.com']

    @staticmethod
    def processed_rude_words():
        if CommentStaticData.processed_rude_word_list is not None:
            return CommentStaticData.processed_rude_word_list

        CommentStaticData.processed_rude_word_list = [word for word in process_text(' '.join(CommentStaticData.rude_word_list)).split(' ') if len(word.strip()) > 0]
        CommentStaticData.processed_rude_word_list.extend([word for word in process_text(' '.join(CommentStaticData.additional_stop_words)).split(' ') if len(word.strip()) > 0])

        print("[Rude word list] %s" % (str(CommentStaticData.processed_rude_word_list)))
        return CommentStaticData.processed_rude_word_list

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
    analysed    = Column(DateTime, default=None)
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
    def comments_for_analysis():
        session = db_session()
        query = session.query(SiteComment).filter(SiteComment.is_verified==False).filter(SiteComment.analysed==None).order_by(desc(SiteComment.creation_date))
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

    @staticmethod
    def analysed_as_rude(limit=30):
        session = db_session()
        query = session.query(SiteComment).filter(SiteComment.analysed!=None).filter_by(looks_rude=True).order_by(desc(SiteComment.creation_date)).limit(limit)
        result = query.all()
        session.close()
        return result    


class JSONObjectData(db.Model):
    __tablename__ = 'json_object_data'
    FEATURE_TYPE_ID = 0
    LOGREG_TYPE_ID  = 1
    
    id          = Column(Integer, primary_key=True)
    type_id     = Column(Integer)
    object_json = Column(String)
    added       = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, type_id, object_json):
        self.type_id    = type_id
        self.object_json= object_json
        self.added      = datetime.datetime.now()

    @staticmethod
    def last(type_id):
        session = db_session()
        query = session.query(JSONObjectData).filter(JSONObjectData.type_id==type_id).order_by(desc(JSONObjectData.added))
        result = query.first()
        session.close()
        return result    
