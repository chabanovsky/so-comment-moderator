# encoding:utf-8
from se_api import get_recent_comments
from db_models import SiteComment, DBModelAdder
from utils import process_text

from tfidf import DocsStats, Document
from cosine_similarity import CosineSimilarity
from naive_bayes_classifier import BinaryNaiveBayesClassifier
from logistic_regression import LogisticRegaression


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
    analyse_with_bayes_classifier()
    #analyse_with_cosine()

def analyse_with_bayes_classifier():
    rude_comments = SiteComment.rude_comments()
    normal_comments = SiteComment.normal_comments()
    
    classifier = LogisticRegaression(True)
    classifier.train(rude_comments, normal_comments)
    rude_total, rude_right, normal_total, normal_right = classifier.test()

    tpr = float(rude_right)/float(rude_total)
    tnr = float(normal_right)/float(normal_total)
    total_objects = float(rude_total + normal_total)
    acc = (rude_right/total_objects) * tpr + (normal_right/total_objects) * tnr

    print("Accuracy: %s, rude: %s (%s), normal: %s (%s) " % (str(acc), str(rude_right), str(rude_total), str(normal_right), str(normal_total)))

    print("Analyse real comments:")    
    unverified_comments = SiteComment.unverified_comments()
    for comment in unverified_comments:
        if classifier.classify_rude(comment.processed_body.split(" ")):
            print(comment.body)


def analyse_with_cosine():
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