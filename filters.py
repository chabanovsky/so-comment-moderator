from sqlalchemy.sql import func, literal_column
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy import and_, desc

from jinja2 import evalcontextfilter, Markup

from meta import app as application, LANGUAGE, db_session, APP_URL

def current_language():
    return LANGUAGE

def app_url():
    return APP_URL

application.jinja_env.globals.update(current_language=current_language,
                                    app_url=app_url)     