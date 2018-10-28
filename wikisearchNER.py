import json
import wikipedia
import time


l =[]
s = ''
a = []
for line in open('NER_blind_test','r'):   #change files names based on dev /test
	if len(line.strip())==0:
		l.append(a)
		a = []
		continue
	if line.strip().split('\t')[-1]=='O':
		if s!='':
			a.append(s)
		s =''
		continue
	if s!='':
		s = s+' '+line.strip().split('\t')[0]
	else:
		s = line.strip().split('\t')[0]


count = 0
for line in open('shared_task_test.jsonl','r'):
	line = json.loads(line)
	claim = line['claim'][:-1]
	print(claim)
	if 'film' in claim.split() or '(film)' in claim.split() or 'film)' in claim.split():
		if 'is' in claim.split():
			l[count].append(claim.split('is')[0]+' '+'film')
		if 'was' in claim.split():
			l[count].append(claim.split('was')[0]+' '+'film')
		if 'in the film' in claim:
			l[count].append(claim.split('in the film')[1]+' '+'film')
		elif '(film)' in claim:
			l[count].append(claim.split('(film)')[0]+' '+'film')
		elif 'film)' in claim:
			l[count].append(claim.split(')')[0]+') ')
		elif 'called' in claim:
			l[count].append(claim.split('called')[1]+' film')
	if 'directed by' in claim:
		if 'is directed by' in claim:
			l[count].append(claim.split('is directed by')[0]+' '+'film')
		elif 'was directed by' in claim:
			l[count].append(claim.split('was directed by')[0]+' '+'film')
	if 'stars' in claim:
		l[count].append(claim.split('stars')[0]+' '+'film')
	if 'is a' in claim and 'film' not in claim:
		l[count].append(claim.split('is a')[0])
	if 'is the' in claim:
		l[count].append(claim.split('is the')[0])
	if 'premiered in' in claim:
		l[count].append(claim.split('premiered in')[0])
	if 'based on' in claim:
		if 'is ' in claim:
			l[count].append(claim.split('is ')[0])
		elif 'are ' in claim:
			l[count].append(claim.split('are ')[0])
	if 'was' in claim and 'film' not in claim:
		l[count].append(claim.split('was')[0])
	if 'has' in claim:
		l[count].append(claim.split('has')[0])
	if 'is' in claim and 'actor' in claim:
		l[count].append(claim.split('is')[0]+' '+'actor')
	if 'is' in claim and 'actress' in claim:
		l[count].append(claim.split('is')[0]+' '+'actress')
	if 'features' in claim:
		l[count].append(claim.split('features')[0])
	count = count+1
	break




count = 1
for a in l:
	f= open('NER_shared_test.txt','a') #change files names based on dev /test
	rec = []
	a = list(set(a))
	for ner in a:
		y = wikipedia.search(ner,1)
		for x in y:
			x = x.replace(' ','_')
			x = x.replace('(','-LRB-')
			x = x.replace(')','-RRB-')
			x = x.replace(':','-COLON-')
			rec.append(x)
	rec = list(set(rec))
	print(rec)
	f.write(json.dumps(rec)+'\n')
	f.close()




