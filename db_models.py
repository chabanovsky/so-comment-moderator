# encoding:utf-8
import datetime
import collections
import csv

import logging

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean, ForeignKey, ColumnDefault, Float
from sqlalchemy import and_, or_, desc, asc, bindparam, text, Interval
from sqlalchemy.sql import func, select, update, literal_column, column, join
from sqlalchemy.dialects.postgresql import aggregate_order_by
from flask.ext.sqlalchemy import Pagination

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
    processed_rude_word_list = None

    rude_word_list = ["жопа","тугадум","отмазка","недоумок","предьява","гандон","говно","студент-халявщик","вопрошайка","lmgtfy","пися","говнецо","ничерта","говкод","студентота","пзд","хамьё","балван","болван","никчёмность","хуй","утырок","мудаки","мудак","аморально","шлюшка","топлёсс","путин","сцук","флейм","мудак","пидор","быдло","поебать","рот","гавнокодер","неадекват","кармадрочерство","олигофрен","хер","ржунимаг","гомосечь","тормаз","ебал","отсос","петушок","кретин","обсёр","срань","слобоумие","шлюха","гопник","дерьмо","хуесос","говносайт","говнокодер","шиза","ебло","говноконтора","гандон","ахинея","пиздец","некроговнокод","нахуя","шизофреник","похер","хуесос","маргинал","жлобство","дурачок","фалос","глупышка","говнарь","клоун","порно","нахуй","пукан","шут","ахуенно","ебанько","дятел","ебеня","хуйня","похуй","хам","писюн","уебок","задрот","писька","блять","мразь","дегенерат","хуев","подонок","ахренеть","слабак","пидарас","гондон","дибилизм","проститутка","ебать","ололоша","девка","бомжара","кармадрочер","чмошник","фриланс-биржа","пизда","убожество","сраный","бездарь","безмозглый","тупизм","гугл","стыдно","стыд","лень","лентяй","за тебя","в гугл","херня","погуглить","гуглить", "гребанный","ебаный","тухлый","убогий","пендосский","блядский","ебанутый","ахуенный","вонючий","рукожопый","ёбаный","ебучая","проебанный","уебаный","ебучий","бляццкий","ленивый","смыться","бухать","просирать","выебываться","сьебаться","срать","потешаться","пыжиться","трахать","быдлокодить","пиздеть","лизать","понтоваться","обосраться","хуярить","дрочить","выбесить","подрочить","отсосать","вздрочнуть","ебануть","стебаться","насосать","нассать","гавнокодить","помастурбировать","полизать","пиздить","ахринеть","обосрать"]
    additional_stop_words = ['fuck', 'наркоман', 'женщина', 'бабло', 'холивар', 'кэп', 'говнокод', 'неадекватен', 'тролль', 'нахрена', 'хрен', 'бля', 'блядь', 'школоло', 'баттхерт', 'нах', 'телепат', 'экстрасенс', 'троллинг', 'умник', 'нихера', 'шняга', 'матчасть', 'впадлу', 'школьник', 'нуб', 'попец', 'хуле', 'з****ли', 'бл**', 'бл*ть', 'на***', 'г**о', 'пиз*ц', 'бл*', 'епта', 'ебн*тый', 'под***ать', 'п*зд*ц', 'поп*й', 'х***', 'дыбил', 'тупой', 'урод', 'телка', 'дурик', 'глупый', 'бред', 'балда', 'дичь', 'хреновина', '**ев', 'чушь', 'ноют', 'ныть', 'заебал', 'долбаеб', 'банальщина', 'дурак', 'обоснуй', 'нах*й', 'хамло', 'отстой', 'тварь', 'козел', 'чмо', 'пидарьё', 'wtf', 'г....о', 'аболтус', 'идиотский', 'идиот', 'чудик', 'хуясебе', 'балабол', 'сосать', 'дебил', 'соизвольте', 'вонючий', 'пзда', 'фуфло', 'грёбанный', 'колхозник', 'дерзить', 'убиться', 'бегом', 'херь', 'малолетка', 'бесполезный', 'кривой', 'дебильная', 'уебки', 'чувак', 'даун', 'очнись', 'дохрена', 'бредово', 'неадекватный', 'омг', 'бестолковый', 'мочер', 'дигенерат', 'некомпетентный', 'дятел', 'bullshit', 'петух', 'нытик', 'поржал', 'пох', 'обоссать', 'ху*ями', 'задница', 'олень', 'пиз*ц', 'чукча', 'тупанул', 'чувачок', 'глупость', 'хамье', 'еврей', 'вахтёр', 'вахтер', 'сиськи', 'шизик', 'аутист', 'бесить', 'отсоси', 'отсасывать', 'пудак', 'тугадум', 'ерунда', 'долдон', 'бляццкие', 'бляцкий', 'посмеялся', 'ересь', 'ерись', 'ебаньки', 'кармодрочер', 'погуглю', 'нубов', 'школа', 'жесть', 'уё*ки', 'ебеня', 'спам', 'минус', 'минусете', 'минусовать', 'ахереть', "руский", "промолчать", "молчать", "учиться", "куришь", "курить", "кури", "детсад", "граммар", "обижаться", "обижаются", "вузах", "вуз", "вузы", "нахер", "холивор", "збс", "кастрировать", "кастрировал", "терпеть", "поиск", "интеллект", "гнать", "чудопрограммист", "нахуа", "жлобскими", "жлоб", "дурацким", "дурацкий", "топку", "топка", "россия", "беларусь", "украина", "белоруссия", "беларуссия", "ржач", "фигею", "гашеный", "пьяны", "пьян", "пьяный", "тыкай", "тыкать", "уволить", "увольнять", "хамством", "хамство", "гитлер", "холуем", "холуй", "сердюков", "кудрин", "ударил", "ударять", "тартар", "*бки", "слабо", "подгорело", "подгорает", "ебет", "гений", "воровать", "туева", "путинский", "мда", "ум", "булшит", "учитель", "анекдот", "разрешаю", "разрешаем", "господи", "мямлить", "болтовни", "болтовня", "борзеть", "борзота", "борзый", "позор", "анальное", "неуч", "несёшь", "уродский", "студенческий", "анал", "трах", "каша", "говнокоммент", "мозг", "п#здец", "врете", "врать", "русский", "базар", "заминусовал", "бан", "пук", "гадать", "диванные", "пукану", "чепуху", "чепуха", "порнуха", "гнида"]    
    serach_links = ['google.com', 'google.ru', 'google.com.ua', 'yandex.ua', 'lmgtfy.com', "tsya.ru"]

    @staticmethod
    def processed_rude_words():
        if CommentStaticData.processed_rude_word_list is not None:
            return CommentStaticData.processed_rude_word_list

        CommentStaticData.processed_rude_word_list = [word for word in process_text(u' '.join(CommentStaticData.rude_word_list)).split(' ') if len(word.strip()) > 0]
        CommentStaticData.processed_rude_word_list.extend([word for word in process_text(u' '.join(CommentStaticData.additional_stop_words)).split(' ') if len(word.strip()) > 0])
        return CommentStaticData.processed_rude_word_list


def paginate_helper(query, page_num, per_page):
    total = query.count()
    items = query.offset((page_num-1)*per_page).limit(per_page).all()
    p = Pagination(query, page_num, per_page, total, items)
    return p

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

    verified    = Column(DateTime, default=None)
    is_rude     = Column(Boolean, default=False)
    verified_user_id= Column(BigInteger)

    added       = Column(DateTime, default=datetime.datetime.now)
    analysed    = Column(DateTime, default=None)
    looks_rude  = Column(Boolean, default=False)
    skipped     = Column(DateTime, default=None)

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

        self.verified   = params.get('verified', None)
        self.is_rude    = params.get('is_rude', False)
        self.verified_user_id = params.get('verified_user_id', -1)
        

        self.added      = params.get('added', datetime.datetime.now())
        self.analysed   = params.get('analysed', None)
        self.looks_rude = params.get('looks_rude', False)
        self.skipped    = params.get('skipped', None)

    def __repr__(self):
        return '<%s %r>' % (SiteComment.__tablename__, str(self.id))

    @staticmethod
    def by_comment_id(comment_id):
        session = db_session()
        query = session.query(SiteComment).filter_by(comment_id=comment_id)
        result = query.first()
        session.close()
        return result

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
        query = session.query(SiteComment).filter(SiteComment.skipped==None).filter(SiteComment.is_rude==True).filter(SiteComment.verified!=None).order_by(desc(SiteComment.creation_date))
        result = query.all()
        session.close()
        return result    

    @staticmethod
    def normal_comments():  
        session = db_session()
        query = session.query(SiteComment).filter(SiteComment.skipped==None).filter(SiteComment.is_rude==False).filter(SiteComment.verified!=None).order_by(desc(SiteComment.creation_date))
        result = query.all()
        session.close()
        return result  

    @staticmethod
    def skipped_comments():
        session = db_session()
        query = session.query(SiteComment).\
            filter(SiteComment.analysed!=None).\
            filter(SiteComment.skipped!=None).\
            order_by(desc(SiteComment.creation_date))
        result = query.all()
        session.close()
        return result  

    @staticmethod
    def comments_for_analysis(analysed_at=None, include_skipped=False):
        session = db_session()
        query = session.query(SiteComment).filter(SiteComment.verified==None)
        if not include_skipped:
            query = query.filter(SiteComment.skipped==None)
        if analysed_at is None:
            query = query.filter(SiteComment.analysed==None)
        else:
            query = query.filter(or_(SiteComment.analysed==None, SiteComment.analysed<analysed_at))
        query = query.order_by(desc(SiteComment.creation_date))
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
    
    @staticmethod
    def paginate_unverified(page_num, per_page=15):
        session = db_session()
        query = session.query(SiteComment).\
            filter(SiteComment.analysed!=None).\
            filter(SiteComment.looks_rude==True).\
            filter(SiteComment.verified==None).\
            filter(SiteComment.skipped==None).\
            order_by(desc(SiteComment.creation_date))
        p = paginate_helper(query, page_num, per_page)
        session.close()
        return p 

    @staticmethod
    def paginate_verified(page_num, per_page=15):
        session = db_session()
        query = session.query(SiteComment).\
            filter(SiteComment.analysed!=None).\
            filter(SiteComment.verified!=None).\
            filter(SiteComment.skipped==None).\
            order_by(desc(SiteComment.verified))
        p = paginate_helper(query, page_num, per_page)
        session.close()
        return p    

    @staticmethod
    def paginate_skipped(page_num, per_page=15):
        session = db_session()
        query = session.query(SiteComment).\
            filter(SiteComment.analysed!=None).\
            filter(SiteComment.skipped!=None).\
            order_by(desc(SiteComment.creation_date))
        p = paginate_helper(query, page_num, per_page)
        session.close()
        return p 

    @staticmethod
    def verified_after(date):
        session = db_session()
        result = session.query(func.count(SiteComment.id)).filter(SiteComment.verified>date).scalar()
        session.close()
        return result    

class JSONObjectData(db.Model):
    __tablename__ = 'json_object_data'
    FEATURE_TYPE_ID = 0
    LOGREG_TYPE_ID  = 1
    
    id          = Column(Integer, primary_key=True)
    type_id     = Column(Integer)
    object_json = Column(String)
    extra       = Column(String)
    added       = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, type_id, object_json, extra=""):
        self.type_id    = type_id
        self.object_json= object_json
        self.added      = datetime.datetime.now()
        self.extra      = extra

    @staticmethod
    def last(type_id):
        session = db_session()
        query = session.query(JSONObjectData).filter(JSONObjectData.type_id==type_id).order_by(desc(JSONObjectData.added))
        result = query.first()
        session.close()
        return result    

    @staticmethod
    def all_extra(type_id, limit=None, offset=None):
        session = db_session()
        query = session.query(JSONObjectData.extra.label('extra'), JSONObjectData.added.label('added')).filter(JSONObjectData.type_id==type_id).order_by(desc(JSONObjectData.added))
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        result = query.all()
        session.close()
        return result    

    @staticmethod
    def paginate_type(type_id, page_num, per_page=2):
        session = db_session()
        query = session.query(JSONObjectData.extra.label('extra'), JSONObjectData.added.label('added')).\
            filter(JSONObjectData.type_id==type_id).\
            order_by(desc(JSONObjectData.added))
        p = paginate_helper(query, page_num, per_page)
        session.close()
        return p  

class User(db.Model):
    __tablename__ = 'user'

    id          = db.Column(db.Integer, primary_key=True)
    account_id  = db.Column(db.Integer, unique=True)
    user_id     = db.Column(db.Integer)
    username    = db.Column(db.String)
    role        = db.Column(db.String)
    is_banned   = db.Column(db.Boolean)
    end_ban_date= db.Column(db.DateTime, nullable=True)
    reputation  = db.Column(db.Integer)
    profile_image   = db.Column(db.String)
    profile_link= db.Column(db.String)

    def __init__(self, account_id, 
            user_id, 
            username, 
            reputation, 
            profile_image, 
            profile_link, 
            role="user", 
            is_banned=False):
        self.account_id = account_id
        self.user_id = user_id
        self.username = username
        self.reputation = reputation
        self.profile_image = profile_image
        self.profile_link = profile_link
        self.role = role
        self.is_banned = is_banned

    def __repr__(self):
        return '<User %r>' % str(self.id)


    @staticmethod
    def get_by_account_id(account_id):
        session = db_session()
        query = session.query(User).filter(User.account_id==account_id)
        result = query.first()
        session.close()
        return result    
