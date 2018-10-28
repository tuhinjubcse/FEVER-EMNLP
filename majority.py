gold_label = open('./dataset/ols/SNLI/labels.test','r')
pred = open('./result_test_10000000.0.txt','r')
lengths = open('./dataset/ols/SNLI/length.test')
l = []
for line in lengths:
	l.append(int(line.strip()))
m = {'entailment': 0,  'contradiction': 1}
m1 = {0:'SUPPORTS',1:'REFUTES'}
y_test = []
y_pred = []
scores = []
support = 0
attack = 0
nei = 0
for line1,line2,line3 in zip(gold_label,pred,open('./dataset/SNLI1/s1.test')):
	y_test.append(m[line1.strip()])
	y_pred.append(int(line2.strip()))
	if y_test[-1]==0:
		support = support+1
	elif y_test[-1]==1:
		nei = nei +1
	else:
		attack = attack + 1
	line3 = line3.strip().split()
	line3.pop()
	line3 = ' '.join(line3)
	scores.append(line3+'.')
print(support,attack,nei)
		
count = 0
i = 0
print(len(y_pred),len(y_test))
import numpy as np
c = 0
ans = 0
f1 = open('predict_test_normal.jsonl','w')
import json
s =0
r = 0
n = 0
tie = 0
v = 0
while i<len(y_pred):
	val = 0
	m = [0,0]
	conf_scores = []
	for j in range(i,i+l[c]):
		if j<len(y_pred):
			m[y_pred[j]] = m[y_pred[j]]+1
			val = val+1
	x = {}
	x['label'] = m1[y_test[i]]
	actual = -1
	flag = False
	if m[1]!=0:
		actual = 1
	else:
		actual = 0
	if actual==1:
		r = r+1
	if actual==y_test[i]:
		count = count+1
		if actual==0:
			s = s+1
		if actual==1:
			n = n+1
	f1.write(m1[actual]+'\t'+scores[i]+'\n')
	i = i+l[c]
	c = c+1
	

print(count,c,s,n,r)
