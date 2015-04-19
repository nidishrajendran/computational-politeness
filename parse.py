from readCsv import *
import subprocess
import nltk.tokenize.punkt

DATA_FILE = "data/stack-exchange.annotated.csv"

def getDocs():
	result = ["Have you found the answer for your question? If yes would you please share it?", "What are you trying to do?  Why can't you just store the \"Range\"?"]
	return result

def getTokenizedSentences(docs):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	result = []
	c = 0
	for d in docs:
		l = sent_detector.tokenize(d)
		if len(l)==2:
			result.append(l)
		else:
			c+=1
	# result = [sent_detector.tokenize(d) for d in docs]
	print c
	return result

def getParses(parsed):
	newStart = 0
	parses, currParse = [], []

	print "Getting parses"
	for p in parsed:
		p = p.strip()
		if p=='':
			continue
		elif p[0]=='(' and newStart==1:
			parses.append(currParse)
			currParse = []
			newStart = 0
		else:
			if newStart==0:
				newStart=1
			currParse.append(p)

	parses.append(currParse)
	return parses

def makeInputForClassifier(text,sentences,parses):
	result = []
	for i in len(sentences):
		dic = {"sentences":sentences[i], "parses":parses[i]}
		result.append(dic)
	return result

docsDic = readcsv(DATA_FILE)
d = docsDic.values()
docs = [unicode(val, "utf-8") for val in d]
# raw_input()
sentences = getTokenizedSentences(docs)
print sentences[0:4]

# parsed = subprocess.check_output(['Jstanparser/lexparser.sh', DATA_FILE]).split("\n")
# parses = getParses(parsed)
# print parses

# classifierInput = makeInputForClassifier(text,sentences,parses)