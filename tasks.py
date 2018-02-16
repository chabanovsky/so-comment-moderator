# encoding:utf-8
import datetime

from se_api import get_recent_comments, get_post_infos
from db_models import SiteComment, DBModelAdder
from utils import process_text

from tfidf import DocsStats, Document
from cosine_similarity import CosineSimilarity
from naive_bayes_classifier import BinaryNaiveBayesClassifier
from logistic_regression import LogisticRegaression

from meta import MODEL_LOGISITIC_REGRESSION, MODEL_NAIVE_BAYES, CURRENT_MODEL



def load_comments_from_se_to_db():
    def make_site_comment_params(comment, info):
        comment_id, post_id, body, creation_date, author_id, author_name = comment
        question_id, answer_id, post_author_id, post_author_name, score, title, post_creation_date = info

        return {
            "comment_id": comment_id,
            "question_id": question_id,
            "answer_id": answer_id,
            "post_author_id": post_author_id,
            "post_score": score,
            "title": title,
            "body": body,
            "processed_body": process_text(body),
            "creation_date": creation_date,
            "author_id": author_id,
            "author_name": author_name,
            "is_verified": False,
            "is_rude": False,
            "diff_with_post": (creation_date - post_creation_date).total_seconds()
        }

    last_one = SiteComment.last_comment()
    comments = get_recent_comments(last_one.creation_date)
    infos = dict()
    ids = [comment[1] for comment in comments]
    page_size = 20
    counter = 0

    while counter < len(ids):
        req_ids = ids[counter:counter+page_size]
        info = get_post_infos(req_ids)
        infos.update(info)
        counter += page_size

    adder = DBModelAdder()
    adder.start()

    for comment in comments:
        if SiteComment.is_exist(adder, comment[0]):
            continue
        adder.add(SiteComment(make_site_comment_params(comment, infos.get(comment[1]))))

    adder.done()

def analyse_comments():
    classifier = None
    if CURRENT_MODEL == MODEL_NAIVE_BAYES:
        classifier = analyse_with_bayes_classifier()
    elif CURRENT_MODEL == MODEL_LOGISITIC_REGRESSION:
        classifier = analyse_with_logistic_regression()

    if classifier is None:
        print ("Classifier is not set up. Set up classifier first.")
        return

    print("Model is ready. Starting analysis...")    
    adder = DBModelAdder()
    adder.start()
    comments_for_analysis = SiteComment.comments_for_analysis()
    for comment in comments_for_analysis:
        comment.analysed = datetime.datetime.now()
        comment.looks_rude = classifier.classify_rude(comment)
        adder.add(comment)
    adder.done()

    print("Analysis was done for %s comments" % (str(len(comments_for_analysis))))        

def analyse_with_bayes_classifier():
    rude_comments = SiteComment.rude_comments()
    normal_comments = SiteComment.normal_comments()

    classifier = BinaryNaiveBayesClassifier(True)
    classifier.train(rude_comments, normal_comments)
    classifier.print_params()

    return classifier

def analyse_with_logistic_regression():
    rude_comments = SiteComment.rude_comments()
    normal_comments = SiteComment.normal_comments()
    
    classifier = LogisticRegaression(rude_comments, normal_comments, True)
    classifier.train()
    rude_total, rude_right, normal_total, normal_right = classifier.test(True)

    tpr = float(rude_right)/float(rude_total)
    tnr = float(normal_right)/float(normal_total)
    total_objects = float(rude_total + normal_total)
    acc = (rude_right/total_objects) * tpr + (normal_right/total_objects) * tnr
    print("Accuracy: %s, rude: %s (%s), normal: %s (%s) " % (str(acc), str(rude_right), str(rude_total), str(normal_right), str(normal_total)))
    
    return classifier

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

    unverified_comments = SiteComment.comments_for_analysis()
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