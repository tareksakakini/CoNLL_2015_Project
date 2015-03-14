import os
from collections import defaultdict

def PopulateVocabulary():
	Vocabulary = defaultdict(int)
	i=0
	training_path = "/media/training-datasets/conll15-st-train-2015-03-04/raw/"
	for filename in os.listdir(training_path):
		#print filename
		#print "aha"
		text = open(training_path+filename,'r')
		for lines in text.readlines():
			for words in lines.split():
				if not(words in Vocabulary) :
					Vocabulary[words]=i
					i+=1
					#print words
					#print filename
	return Vocabulary

Vocab = PopulateVocabulary()
print Vocab['the']
print Vocab['hence']
print Vocab['girl']	
print len(Vocab)
