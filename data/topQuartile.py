import csv
filename="wikipedia.annotated.csv"

f = open(filename)
csv_f = csv.reader(f)
text_corpus=[]
csv_f.next()
for row in csv_f:
    text_corpus.append((row[2],float(row[-1])))
text_corpus.sort(key=lambda l: l[1])
top=[]
for i in range(len(text_corpus)/4):
    top.append(i)

