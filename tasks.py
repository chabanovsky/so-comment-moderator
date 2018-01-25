# encoding:utf-8
from se_api import get_recent_comments
from db_models import SiteComment, DBModelAdder
from utils import process_text

from tfidf import DocsStats, Document
from cosine_similarity import CosineSimilarity


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
    

def analyse_comments():
    stats = DocsStats()
    rude_comments = SiteComment.rude_comments()
    rude_docs = list()
    for comment in rude_comments:
        rude_docs.append(
            Document(stats, 
                    comment.id, 
                    comment.body, 
                    comment.processed_body)
        )

    unverified_comments = SiteComment.unverified_comments()
    unverified_docs = list()
    for comment in unverified_comments:
        unverified_docs.append(
            Document(stats, 
                    comment.id, 
                    comment.body, 
                    comment.processed_body)
        )

    stats.calculate_idfs()
    stats.vectorise_documents()

    cosine = CosineSimilarity(rude_docs)
    rude_cluster = cosine.biggest_cluster()
    for item in rude_cluster:
        print("- ", item.body, "\r\n")
    
