# encoding:utf-8
from se_api import get_recent_comments
from db_models import SiteComment, DBModelAdder
from utils import process_text

from tfidf import DocsStats, Document
from cosine_similarity import CosineSimilarity
from naive_bayes_classifier import BinaryNaiveBayesClassifier


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

    k = 0.8
    rude_comments_len = len(rude_comments)
    train_rude_len = int(rude_comments_len * k)
    train_normal_len = int(len(normal_comments) * k)

    train_rude_comments = rude_comments[:train_rude_len]
    train_normal_comments = normal_comments[:train_normal_len]

    test_rude_comments = rude_comments[train_rude_len:]
    test_normal_comments = normal_comments[train_normal_len:]

    classifier = BinaryNaiveBayesClassifier()
    classifier.train(train_rude_comments, train_normal_comments, rude_comments_len, SiteComment.TotalNumberOfComments-rude_comments_len)

    print ("\r\nRude comments to test: %s" % (str(len(test_rude_comments))))
    print ("Testing...")
    rude_count = 0
    for comment in test_rude_comments:
        if classifier.classify_rude(comment.processed_body.split(" ")):
            rude_count += 1

    print ("Classified as rude: %s\r\n" % (str(rude_count)))
    print ("Normal comments to test: %s" % (str(len(test_normal_comments))))
    print ("Testing...")

    normal_count = 0
    for comment in test_normal_comments:
        if not classifier.classify_rude(comment.processed_body.split(" ")):
            normal_count += 1
            
    print ("Classified as normal: %s\r\n" % (str(normal_count)))

    print("Analyse others")    
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