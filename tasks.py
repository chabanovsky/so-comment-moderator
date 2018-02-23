# encoding:utf-8
import datetime
import json

from se_api import get_recent_comments, get_post_infos
from db_models import SiteComment, DBModelAdder, JSONObjectData
from utils import process_text

from tfidf import DocsStats, Document
from cosine_similarity import CosineSimilarity
from naive_bayes_classifier import BinaryNaiveBayesClassifier
from logistic_regression import LogisticRegaression
from features import SiteCommentFeatures
from feature_list import SiteCommentFeatureList

from meta import MODEL_LOGISITIC_REGRESSION, MODEL_NAIVE_BAYES, CURRENT_MODEL, REBUILD_MODEL_THRESHOLD

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
            "verified": None,
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

def check_to_rebuild():
    saved_data = JSONObjectData.last(JSONObjectData.LOGREG_TYPE_ID)
    feature_saved_data = JSONObjectData.last(JSONObjectData.FEATURE_TYPE_ID)
    if saved_data is None or feature_saved_data is None:
        print("There are no saved data. Starting rebuilding...")
        create_model()
        print("Now, do analysis for previous comments with the new model...")
        analyse_comments(datetime.datetime.now())
        return 

    unseen_for_model = SiteComment.verified_after(saved_data.added)
    print("There are currently %s comments which the model has not seen. The threshold is %s" % ( str(unseen_for_model), str(REBUILD_MODEL_THRESHOLD) ))
    if unseen_for_model >= REBUILD_MODEL_THRESHOLD:
        print("We are above the threshold. Starting rebuilding...")
        create_model()
        print("Now, do analysis for previous comments with the new model...")
        analyse_comments(datetime.datetime.now())
        return 

    print("No reason to rebuild. We will wait a bit more.")

def create_model():
    if CURRENT_MODEL == MODEL_LOGISITIC_REGRESSION:
        feature_list = SiteCommentFeatureList(
            SiteComment.rude_comments(), 
            SiteComment.normal_comments()
        )
        feature_maker = feature_list.maker()

        classifier = LogisticRegaression(feature_list, feature_maker, True)
        classifier.train()
        rude_total, rude_right, normal_total, normal_right = classifier.test(True)

        tpr = float(rude_right)/float(rude_total)
        tnr = float(normal_right)/float(normal_total)
        total_objects = float(rude_total + normal_total)
        acc = (rude_right/total_objects) * tpr + (normal_right/total_objects) * tnr
        print("Accuracy: %s, rude: %s (%s), normal: %s (%s) " % (str(acc), str(rude_right), str(rude_total), str(normal_right), str(normal_total)))
        adder = DBModelAdder()
        adder.start()
        
        feature_data = feature_maker.store()
        json_fd = JSONObjectData(JSONObjectData.FEATURE_TYPE_ID, json.dumps(feature_data))
        adder.add(json_fd)
        
        classifier_data = classifier.store()
        classifier_extra = {
            "acc": acc,
            "rude_right": rude_right,
            "rude_total": rude_total,
            "normal_right": normal_right,
            "normal_total": normal_total
        }
        json_cd = JSONObjectData(
            JSONObjectData.LOGREG_TYPE_ID, 
            json.dumps(classifier_data), 
            json.dumps(classifier_extra)
        )
        adder.add(json_cd)

        adder.done()
        print("A new logistic regression classifier was added to the DB.")
    else:
        print("Please specify a model to create first.")

def analyse_comments(analysed_at=None):
    classifier = None
        
    if CURRENT_MODEL == MODEL_LOGISITIC_REGRESSION:
        classifier = analyse_with_logistic_regression()     

    if classifier is None:
        print ("Classifier is not set up. Set up classifier first.")
        return

    print("Model is ready. Starting analysis...")    
    suspected = 0
    adder = DBModelAdder()
    adder.start()
    comments_for_analysis = SiteComment.comments_for_analysis(analysed_at)
    for comment in comments_for_analysis:
        comment.analysed = datetime.datetime.now()
        comment.looks_rude = classifier.classify_rude(comment)
        adder.add(comment)
        if comment.looks_rude:
            suspected += 1
    adder.done()

    print("Analysis was done for %s comments, %s suspected to be rude." % (str(len(comments_for_analysis)), str(suspected) ))        

def analyse_with_bayes_classifier():
    rude_comments = SiteComment.rude_comments()
    normal_comments = SiteComment.normal_comments()

    classifier = BinaryNaiveBayesClassifier(True)
    classifier.train(rude_comments, normal_comments)
    classifier.print_params()

    return classifier

def analyse_with_logistic_regression():
    saved_data = JSONObjectData.last(JSONObjectData.LOGREG_TYPE_ID)
    feature_saved_data = JSONObjectData.last(JSONObjectData.FEATURE_TYPE_ID)
    if saved_data is None or feature_saved_data is None:
        return None
    print(
        "Restoring a logistic regression classifyer. The classifyer id: %s from %s; features: id %s, from %s" 
            % ( 
                str(saved_data.id), 
                str(saved_data.added.strftime("%d %b %Y %H:%M:%S")), 
                str(feature_saved_data.id), 
                str(feature_saved_data.added.strftime("%d %b %Y %H:%M:%S")) 
            ) 
    )
    feature_maker = SiteCommentFeatures.restore(json.loads(feature_saved_data.object_json), True)
    classifier = LogisticRegaression.restore(json.loads(saved_data.object_json), feature_maker, True)
    
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