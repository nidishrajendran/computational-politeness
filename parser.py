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


def picklePaperData():
    csvs = ['wikipedia.annotated.csv', 'stack-exchange.annotated.csv']
    allDetails = [{},{}]
    ind = 1
    with open(csvs[ind]) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['score'] = float(row['Normalized Score'])
            del row['Normalized Score']
            if row['Id'] in allDetails[ind]:
                allDetails[ind][row['Id']+row['Community']] = row
            else:
                allDetails[ind][row['Id']] = row
    print len(allDetails[ind])


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

    parsed = allDetails[ind]
    pickle.dump(parsed, open( "se_parsed.p", "wb" ))


def pickleStretchData():
    allDetails = pickle.load(open('reddit_data.pickle','rb'))
    US_subs = ['usnews', 'unitedstates', 'uspolitics']
    UK_subs = ['unitedkingdom','ukpolitics','uknews']

    result = {'US':{},'UK':{}}
    for sub, val in allDetails.iteritems():
        print sub
        newd = {}
        
        i = 0
        for req in val[1]:
            if i%100==0:
                print i
            dic = corenlp.raw_parse(req['Request'])
            
            l = [sent['indexeddependencies'] for sent in dic['sentences']]
            req['parses'] = getParses(l)

            l = [sent['text'].encode('ascii','ignore') for sent in dic['sentences']]
            req['sentences'] = l
            
            newd[req['id'].encode('ascii','ignore')] = req
            i+=1
            
        if sub in US_subs:
            result['US'][sub] = newd
        else:
            result['UK'][sub] = newd

    pickle.dump(result, open( "reddit_parsed.p", "wb" ) )


# picklePaperData()
# pickleStretchData()