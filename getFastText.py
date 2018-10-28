import fastText

model = fastText.load_model('./sentence/wiki.en.bin')
f = open('embedding.txt','w')
for line in open('word_dict.txt','r'):
	line = line.strip()
	s = ''
	vec = []
	x = model.get_word_vector(line)
	for a in x:
		vec.append(str(a))
	s = ' '.join(vec)
	f.write(line+'\t'+ s+'\n')
import ast
#for line in open('embedding.txt','r'):
#	line = line.strip().split('\t')
#	print(ast.literal_eval(line[1]))
#	break
