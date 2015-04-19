import cPickle as pickle

from nltk import word_tokenize,sent_tokenize

def unpickle(filename):
    f = open(filename,"rb") 
    heroes = pickle.load(f)
    return heroes

def writePickle(struct, filename):
    file1 = open(filename,"wb")             
    pickle.dump(struct,file1)
    file1.close()

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

reddit_data_news = unpickle("reddit_data_news.pickle")
reddit_data_politics = unpickle("reddit_data_politics.pickle")
reddit_data_countries = unpickle("reddit_data_countries.pickle")

result = merge_dicts(reddit_data_news,reddit_data_countries,reddit_data_politics)
writePickle(result,"reddit_data.pickle")
for word in result:
	print word
	print len(result[word][1])