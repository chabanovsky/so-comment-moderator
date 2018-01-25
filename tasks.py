# encoding:utf-8
from se_api import get_recent_comments
from db_models import SiteComment, DBModelAdder
from utils import process_text


def load_comments_from_se_to_db():
    last_one = SiteComment.last_comment()
    comments = get_recent_comments(last_one.creation_date)

    adder = DBModelAdder()
    adder.start()
    for comment_id, post_id, body, creation_date, author_id in comments:
        if SiteComment.is_exist(adder, comment_id):
            continue
        
        adder.add(
            SiteComment(comment_id, 
                        post_id, 
                        body, 
                        process_text(body), 
                        creation_date, 
                        False, False, 
                        author_id)
        )

    adder.done()
    