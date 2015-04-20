import numpy as np
import matplotlib.pyplot as plt
import csv
import pickle
import random as random
import pickle as cPickle
from sklearn import svm
from scipy.sparse import csr_matrix
from sklearn.metrics import classification_report
from features.vectorizer import PolitenessFeatureVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn import cross_validation


stack_data=pickle.load(open('data/se_parsed.p'))
wiki_data=pickle.load(open('data/wiki_parsed.p'))

def chuckNeutralRequests(docs):
    print "Chucking neutral requests"
    vals = docs.values()
    vals.sort(key=lambda l: l['score'])
    # l = []
    # for v in vals:
    #     l.append(v['score'])
    # l = np.array(l)
    # print l
    n = len(vals)
    # n1 = vals[0:n/4]
    # n2 = vals[(3*n/4):]
    # print n, len(n1), len(n2) 
    return vals[0:n/4] + vals[(3*n/4):]
    # raw_input()

def documents2feature_vectors(documents):
    vectorizer = PolitenessFeatureVectorizer()
    fks = False
    X, y = [], []
    for d in documents:
        fs = vectorizer.features(d)
        if not fks:
            fks = sorted(fs.keys())
        fv = [fs[f] for f in fks]
        # If politeness score > 0.0, 
        # the doc is polite, class=1
        l = 1 if d['score'] > 0.0 else 0
        X.append(fv)
        y.append(l)
    X = csr_matrix(np.asarray(X))
    y = np.asarray(y)
    return X, y

bow = 10
def crossdomain(documents_stack, documents_wiki):
    print "Cross Domain"
    # documents_stack=stack_data.values() 
    # documents_wiki=wiki_data.values()
    PolitenessFeatureVectorizer.generate_bow_features(documents_stack, bow)

    X_stack, y_stack = documents2feature_vectors(documents_stack)
    X_wiki, y_wiki = documents2feature_vectors(documents_wiki)

    print "Fitting"
    clf = svm.SVC(C=0.02, kernel='linear', probability=True)
    # clf = RandomForestClassifier(n_estimators=50)
    clf.fit(X_stack, y_stack)
    y_pred = clf.predict(X_wiki)
    print "Trained on Stack and results predicted for wiki" 
    # Test
    #print(classification_report(y_wiki, y_pred))
    print(clf.score(X_wiki, y_wiki))

    print "------------------------------------------------------"

    PolitenessFeatureVectorizer.generate_bow_features(documents_wiki, bow)

    X_stack, y_stack = documents2feature_vectors(documents_stack)
    X_wiki, y_wiki = documents2feature_vectors(documents_wiki)

    print "Fitting"
    clf = svm.SVC(C=0.02, kernel='linear', probability=True)
    # clf = RandomForestClassifier(n_estimators=50)
    clf.fit(X_wiki, y_wiki)
    y_pred = clf.predict(X_stack)
    print "Trained on wiki and results predicted for stack" 
    # Test
    #print(classification_report(y_stack, y_pred))
    print(clf.score(X_stack, y_stack))
    print "------------------------------------------------------"



def indomain(documents_stack, documents_wiki):
    print "In Domain"
    
    PolitenessFeatureVectorizer.generate_bow_features(documents_stack, bow)

    X_stack, y_stack = documents2feature_vectors(documents_stack)
    
    print "Fitting"
    clf = svm.SVC(C=0.02, kernel='linear', probability=True)
    scores = cross_validation.cross_val_score(clf, X_stack, y_stack, cv=10)
    print "In doman for stack"
    print scores
    print np.mean(scores)

    print "------------------------------------------------------"

    PolitenessFeatureVectorizer.generate_bow_features(documents_wiki, bow)
    X_wiki, y_wiki = documents2feature_vectors(documents_wiki)
    print "Fitting"
    clf = svm.SVC(C=0.02, kernel='linear', probability=True)
    scores = cross_validation.cross_val_score(clf, X_wiki, y_wiki, cv=10)
    print "In doman for wiki"
    print scores

    print "Mean: ", np.mean(scores)


top_stack_data = chuckNeutralRequests(stack_data)
top_wiki_data = chuckNeutralRequests(wiki_data)
#crossdomain(top_stack_data, top_wiki_data)
indomain(top_stack_data, top_wiki_data)

