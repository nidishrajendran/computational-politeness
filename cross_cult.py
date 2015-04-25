import pickle
import math
import numpy as np
from scipy.sparse import csr_matrix
from features.vectorizer import PolitenessFeatureVectorizer

MODEL_FILENAME = 'politeness-svm.p'
clf = pickle.load(open(MODEL_FILENAME,'rb'))
vectorizer = PolitenessFeatureVectorizer()

def documents2feature_vectors(documents):
	print "Generating feature vectors"
	X= []
	for d in documents:
		fs = vectorizer.features(d)
		fks = sorted(fs.keys())
		fv = [fs[f] for f in fks]
		X.append(fv)
	X = csr_matrix(np.asarray(X))
	return X

def getScores(sub):
	# sub should be a list of requests 
	# each having indexed deps and tokenized sentences
	X = documents2feature_vectors(sub)
	scores = clf.predict(X)
	return scores

# DATA_FILE = 'data/reddit_parsed.p'
# redditData = pickle.load(open(DATA_FILE,'rb'))

# predictions = {'US':{},'UK':{}}
# for country, subs in redditData.iteritems():
# 	result = {}
# 	for sub, data in subs.iteritems():
# 		print "Getting scores for subreddit -", sub, "with", len(data), "requests" 
# 		result[sub] = getScores(data)
# 	predictions[country] = result

# for country, subs in predictions.iteritems():
# 	for sub, scores in subs.iteritems():
# 		print sub, np.mean(scores)



def getMeanScores(pickle_in):
	redditData = pickle.load(open(pickle_in,'rb'))
	predictions = dict.fromkeys(redditData.keys())
	for sub, reqs in redditData.iteritems():
		print "Getting scores for subreddit -", sub, "with", len(reqs[1]), "requests" 
		predictions[sub] = getScores(reqs[1])

	# Population stats
	n, u0 = 0, 0.0
	for sub, scores in predictions.iteritems():
		n += len(scores)
		u0 += np.sum(scores)
	u0 = u0/n
	print "Total n =", n, "U0 = ", u0

	# t-vals
	for sub, scores in predictions.iteritems():
		print "\n======", sub, "=======\n"
		n_sub = len(scores)
		print "\nn =", n_sub
		s = np.sqrt(np.sum(np.square(scores - u0)) / float(n_sub-1))
		print "s =", s
		x_dash = np.mean(scores)
		print "x_dash =", x_dash
		t = (x_dash - u0)/(s/n_sub)
		print "t =", t

	# average politeness of each subreddit
	for sub, scores in predictions.iteritems():		
		print sub, " - ", np.mean(scores)

DATA_PATH = 'data/parsed/'
# getMeanScores(DATA_PATH+'reddit_us_ind_parsed.p')
# getMeanScores(DATA_PATH+'reddit_atlanta_london_parsed.p')
# getMeanScores(DATA_PATH+'reddit_newyork_sf_parsed.p')
getMeanScores(DATA_PATH+'reddit_religion_parsed.p')
# getMeanScores(DATA_PATH+'reddit_lib_cons_parsed.p')