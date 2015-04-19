import praw, cPickle as pickle
from collections import Counter
from nltk import word_tokenize,sent_tokenize

def unpickle(filename):
    f = open(filename,"rb") 
    heroes = pickle.load(f)
    return heroes

def writePickle(struct, filename):
    file1 = open(filename,"wb")             
    pickle.dump(struct,file1)
    file1.close()


r = praw.Reddit(user_agent='getting political stuff')
r.login('css-throwaway','csspassword')

linebreak = '-----==----==---==-----'

# this may take a while. start early.
def getThreads(subreddit,num_comments=10,max_threads=5000,max_comments=100,min_comments=10,verbose=False):
    comment_counter = 0
    already_done = [] #keep track of threads you've already seen (you can get them twice)
    subred = r.get_subreddit(subreddit) #get a subreddit
    comments = []
    questionComment = []
    for sub in subred.get_top_from_year(limit=max_threads):
        if sub.id not in already_done and comment_counter < num_comments:
            already_done.append(sub.id)
            sub.replace_more_comments(limit=20, threshold=1)
            flat_comments = praw.helpers.flatten_tree(sub.comments)
            for comment in flat_comments:
                diff_comment = True
                for sentence in sent_tokenize(comment.body):              
                    comments.append(sentence) 
                    if '?' in sentence:
                        s = {}
                        if diff_comment:
                            s['before'] = comments[-2]
                        else:
                            s['before'] = ''
                        s['current'] = sentence
                        questionComment.append(s)          
                        comment_counter += 1
                        print 'Added comment. The counter is at',comment_counter
                        diff_comment = False
                    if comment_counter>num_comments:
                        return [comments,questionComment]
    return [comments,questionComment]
thread_names = ['unitedstates','unitedkingdom']

reddit_data = {}
for thread_name in thread_names:
    print thread_name
    reddit_data[thread_name] = getThreads(thread_name,num_comments=1200,max_threads=5000,max_comments=100,min_comments=0,verbose=True)
    writePickle(reddit_data,"reddit_data_countries.pickle")