import json


#Takes all sentences from the blind test jsonl and writes to a file blind_test.txt 
#and then calls pretrained model to get the Named entities and stores them in file in order 


f = open('NER_dev_txt','w')
from allennlp.service.predictors import Predictor
predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/ner-model-2018.04.26.tar.gz")
for line in open('NER_shared_dev','r'):
	line = line.strip()
	results = predictor.predict(sentence=line[0])
	for word, tag in zip(results["words"], results["tags"]):
		f.write(word+'\t'+tag+'\n')
	f.write('\n')
