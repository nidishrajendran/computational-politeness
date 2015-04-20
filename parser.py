#######################################
# This file must be run in the same 
# location as corenlp.py
########################################

from corenlp import StanfordCoreNLP
import pickle
import csv

corenlp_dir = "stanford-corenlp-full-2015-01-29"
corenlp = StanfordCoreNLP(corenlp_dir) # wait a few minutes...
print "\n===StanfordCoreNLP server started===\n"

csvs = ['wikipedia.annotated.csv', 'stack-exchange.annotated.csv']
allDetails = [{},{}]
ind = 1
with open(csvs[ind]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['score'] = float(row['Normalized Score'])
        del row['Normalized Score']
        allDetails[ind][row['Id']] = row
print len(allDetails[ind])

def getParses(inddeps):
    result = []
    for inddep in inddeps:
        new = []
        for tups in inddep:
            a = tups[0].encode('ascii','ignore')
            b = tups[1].encode('ascii','ignore')
            c = tups[2].encode('ascii','ignore')
            comb = a + '(' + b + ', ' + c + ')'
            new.append(comb)
        result.append(new)
    return result

i = 0
for reqid, req in allDetails[ind].iteritems():
    if i%50==0:
        print i
    dic = corenlp.raw_parse(req['Request'])
    
    l = [sent['indexeddependencies'] for sent in dic['sentences']]
    req['parses'] = getParses(l)

    l = [sent['text'].encode('ascii','ignore') for sent in dic['sentences']]
    req['sentences'] = l
    i += 1
#     print req
#     raw_input()

wiki_parsed = allDetails[ind]
pickle.dump(wiki_parsed, open( "se_parsed.p", "wb" ))