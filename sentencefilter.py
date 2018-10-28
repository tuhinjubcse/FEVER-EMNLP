import json
import nltk
from string import punctuation
import sklearn
from sklearn.model_selection import train_test_split
#from keras.preprocessing.sequence import pad_sequences
#from keras.utils import np_utils
#from keras.layers import Conv1D, MaxoutDense,Dense,MaxPooling1D,GaussianNoise, Embedding, Merge, Dropout, LSTM, GRU, Bidirectional, TimeDistributed,Flatten,Activation
import numpy as np
import gensim
from sklearn.metrics import classification_report , precision_recall_fscore_support,precision_score,recall_score,f1_score,confusion_matrix
#from keras.models import Sequential ,Model
#from keras.constraints import maxnorm
#from keras.regularizers import l2
#from keras.utils.np_utils import to_categorical
import math
import sys
# from retrieval.fever_doc_db import FeverDocDB
import os
from allennlp.commands.elmo import ElmoEmbedder
from scipy import spatial
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))







def clean_sentence(line):
        line = line.replace('-LRB-','(')
        line = line.replace('-RRB-',')')
        line = line.replace('-LSB-','{')
        line = line.replace('-RSB-','}')
        line = line.replace('-COLON-',':')
        return line

def jaccard_sim(claim1,claim2):
        x = claim1.lower().split()
        y = claim2.lower().split()
        x1 = []
        y1 = []
        for w in x:
                if w not in stop_words:
                        x1.append(w)
        for w in y:
                if w not in stop_words:
                        y1.append(w)
        num = len(set(x1).intersection(set(y1)))
        # den = len(set(x1).union(set(y1)))
        return num

f1 = open('s1.dev','w')
f2 = open('s2.dev','w')
f3 = open('labels.dev','w')
f4 = open('length.dev','w')

ee = ElmoEmbedder()

count = 1
for line1,line2 in zip(open('dev_new.p3.s10.jsonl','r'),open('document_dev.txt','r')):
        s = ""
        line1 = json.loads(line1)
        line2 = json.loads(line2)['sentences']
        claim = ee.embed_sentence(clean_sentence(line1['claim']).split())[2,0,:]
        s = ''
        vals = []
        print(clean_sentence(line1['claim'])+'\n')
        for i in range(min(5,len(line2))):
                premise = ee.embed_sentence(clean_sentence(line2[i]['sentence']).split())[2,0,:]
                vals.append((1 - spatial.distance.cosine(claim,premise),i,clean_sentence(line2[i]['sentence'])))
                print(clean_sentence(line2[i]['sentence']), vals[i][0])
        vals = list(sorted(vals,  key=lambda elem: (-elem[0],elem[1])))
        if len(vals)==0:
                f1.write(clean_sentence(line1['claim'][:-1]+' .')+'\n')
                f2.write(clean_sentence("Not Enough info for this claim .")+'\n')
                f4.write(str(1)+'\n')
                #if line1['label']=='SUPPORTS':
                f3.write('neutral'+'\n')
                m = {}
        else:
                for i in range(min(3,len(vals))):
                        f1.write(clean_sentence(line1['claim'][:-1]+' .')+'\n')
                        f2.write(clean_sentence(vals[i][2])+'\n')
                        f3.write('neutral'+'\n')
                f4.write(str(min(3,len(vals)))+'\n')
        count = count+1
