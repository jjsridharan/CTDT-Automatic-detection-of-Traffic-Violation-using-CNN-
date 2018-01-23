import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import random
import pickle
from collections import Counter

lemmatizer= WordNetLemmatizer()
hm_lines =100000

def create_lex(pos,neg) :
	lexicon = []
	for fi in [pos,neg] :
		with open(fi,'r') as f:	
			contents = f.readlines()
			for line in contents[ : hm_lines ] :
					all_words=word_tokenize(line.lower())
					lexicon+=list(all_words)
	lexicon= [lemmatizer.lemmatize(i) for i in lexicon]
	w_counts = Counter(lexicon)
	l2=[]
	for w in w_counts :
		if(1000 > w_counts[w] > 50) :
			l2.append(w)
	return l2
def sample_handling(sample,lexicon,classification) :
	featureset = []
	with open(sample,'r') as f:
		contents =f.readlines()
		for l in contents :
			all_words =word_tokenize(l.lower())
			all_words = [lemmatizer.lemmatize(i) for i in all_words]
			features = np.zeros(len(lexicon))
			for word in all_words :
				if(word in lexicon) :
					index = lexicon.index(word.lower())
					features[index]+=1
			features= list(features)
			featureset.append([features,classification])
	return featureset
def create_featureset(pos,neg,test_size=0.1) :
	lexicon = create_lex(pos,neg)
	features =[]
	features+=sample_handling('pos.txt',lexicon,[1,0])
	features+=sample_handling('neg.txt',lexicon,[0,1])
	random.shuffle(features)
	features=np.array(features)
	
	test_size =int(test_size*len(features))
	train_x = list(features[:,0][:-test_size])	
	train_y = list(features[:,1][:-test_size])
	test_x = list(features[:,0][-test_size:])	
	test_y = list(features[:,1][-test_size:])
	return train_x,train_y,test_x,test_y

train_x,train_y,test_x,test_y=create_featureset('pos.txt','neg.txt')
with open('sentiment_set.pickle','wb') as f:
	pickle.dump([train_x,train_y,test_x,test_y],f)

