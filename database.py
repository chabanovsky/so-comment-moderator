from meta import db, db_session, engine
#from db_models import Reviewer, Flagger, SuggestionEditor, ActiveUser, Answer, Question, Visitor, Voter

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    db.create_all()
