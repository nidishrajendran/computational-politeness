import csv
import sys
def readcsv(filename):
    f = open(filename)
    csv_f = csv.reader(f)
    text_corpus={}
    for row in csv_f:
        text_corpus[row[1]]=row[2]
    return text_corpus

text_dict=readcsv('data/stack-exchange.annotated.csv')
for key in text_dict:
    print text_dict[key]
if __name__="main":
    filename='data/stack-exchange.annotated.csv'
    
    if len(sys.argv)>1:
        filename=sys.argv[1]
    text_dict=readcsv(filename)
    for key in text_dict:
    print text_dict[key]

# for i in a:
#     print i,a[i]
#     raw_input()
