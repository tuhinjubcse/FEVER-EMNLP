import json
import nltk
import wikipedia
import ast
import json
import unicodedata


count = 1
for line in open('shared_task_dev.jsonl','r'):
	line = json.loads(line.strip())
	claim = nltk.word_tokenize(line['claim'])
	pos = nltk.pos_tag(claim)
	s = ''
	for w,p in zip(claim,pos):
		if p[1][0]=='V' and w.islower():
			s = s[:-1]
			break
		s = s+ w + ' '
	entity = wikipedia.search(s,1)
	print(entity,count)
	if len(entity)>0:
		f.write(json.dumps([entity[0]])+'\n')
	else:
		f.write(json.dumps([])+'\n')
	count = count+1
