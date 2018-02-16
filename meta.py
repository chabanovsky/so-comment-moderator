import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from local_settings import FLASK_SECRET_KEY, PG_NAME_PASSWORD

def make_db_session(engine):
    return scoped_session(sessionmaker(autocommit=False,
        autoflush=True,
        bind=engine))    

def make_db_engine():
    return create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)

LANGUAGE = "ru"
APP_URL = "http://benice.rudevs.ru"
DB_NAME = "comment_moderator"
FEED_APP_TITLE = ""
SO_URL = "https://%stackoverflow.com" % (str(LANGUAGE + ".") if LANGUAGE != "en" else "")

MODEL_NAIVE_BAYES = 0
MODEL_LOGISITIC_REGRESSION = 1
CURRENT_MODEL = MODEL_LOGISITIC_REGRESSION

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://' + PG_NAME_PASSWORD + '@localhost:5432/'+ DB_NAME + '?client_encoding=utf8'
app.config['BABEL_DEFAULT_LOCALE'] = LANGUAGE

engine = make_db_engine()
db_session = make_db_session(engine)

db = SQLAlchemy(app)           

STACKEXCHANGE_CLIENT_SECRET = os.environ.get("STACKEXCHANGE_CLIENT_SECRET", "")
STACKEXCHANGE_CLIENT_KEY = os.environ.get("STACKEXCHANGE_CLIENT_KEY", "")
STACKEXCHANGE_CLIENT_ID = int(os.environ.get("STACKEXCHANGE_CLIENT_ID", 0)) 