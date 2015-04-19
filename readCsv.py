import csv

def readcsv(filename):
    f = open(filename)
    csv_f = csv.reader(f)
    text_corpus={}
    for row in csv_f:
        text_corpus[row[1]]=row[2]
    return text_corpus

# a=readcsv('data/stack-exchange.annotated.csv')
# for i in a:
#     print i,a[i]
#     raw_input()
