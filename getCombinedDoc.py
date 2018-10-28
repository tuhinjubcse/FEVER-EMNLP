import ast
import json
import nltk
from nltk.corpus import stopwords
import unicodedata
stop_words = set(stopwords.words('english'))

m = {}
discard = {}
vals = ['British_Academy_Film_Awards','BAFTA_Award_for_Best_Film',
			 'BAFTA_Award_for_Most_Promising_ Newcomer_to_Leading_Film_Roles' ,"Satellite_Award_for_Best_Original_Screenplay", "Academy_Award_for_Best_Original_ Screenplay", 
			 "Satellite_Awards", "BAFTA_Award_for_Best_Original_Screenplay", "Satellite_Award_for_Best_Actor_\u2013_Motion_Picture", "Academy_Award_for_Best_Original_Screenplay",
			 "BAFTA_Award_for_Best_Actor_in_a_Leading _Role", "BAFTA_Award_for_Best_Actress_in_a_ Leading_Role","British_Academy_Games_Award_for_Best_ Game",
			 "Academy_Award_for_Best_Sound_Mixing","Academy_Award_for_Best_Animated_Feature","Academy_Award_for_Best_Documentary_Feature",
			 "Independent_Spirit_Award_for_Best_Documentary_Feature", "Golden_Globe_Award_for_Best_Supporting_Actress_\u2013_Motion_Picture", "Academy_Award_for_Best_Supporting_Actress"
			 "Saturn_Award_for_Best_Horror_Television_ Series", "44th_Saturn_Awards", "Saturn_Award", "Saturn_Award_for_Best_Make-up", "Academy_Award_for_Best_Visual_Effects", "Best_Special_Effects",
			 "Academy_Award_for_Best_Makeup_and_Hairstyling","Academy_Award_for_Best_Sound_Editing", "Best_Original_Score", "Academy_Award_for_Best_Original_Score", "Satellite_Award_for_Best_Actor_\u2013_Motion_Picture",
			 "Satellite_Awards","Satellite_Award_for_Best_Cinematography", "Best_Original_Score", "Academy_Award_for_Best_Original_Score", "Satellite_Award_for_Best_Actor_\u2013_Motion_Picture", "Satellite_Awards",
			 "Academy Awards in Best Director","Academy_Awards","70th_British_Academy_Film_Awards","Academy_Award_for_Best_Supporting_Actor","Academy_Award_for_Best_Original_Score","Academy_Award_for_Best_Supporting_Actress",
			 "Saturn_Award_for_Best_Supporting_Actress_ on_Television", "Saturn_Award_for_Best_Supporting_Actor_on _Television",
			 "Academy_Award_for_Best_Original_Song", "Academy_Award_for_Best_Original_Score","Golden_Globe_Award_for_Best_Actor_\u2013_ Motion_Picture_Musical_or_Comedy",
			 "Golden_Globe_Award_for_New_Star_of_the_ Year_\u2013_Actress", "Golden_Globe_Award", "Screen_Award_for_Best_Male_Debut", "Screen_Award_for_Best_Female_Debut", "75th_Golden_Globe_Awards",
			 "Golden_Globe_Award"]
for v in vals:
	discard[v]=True
coun = 1
size = 0


for line1,line2,line3,line4 in zip(open('shared_dev_google.txt'),open('NER_shared_dev.txt'),open('shared_dev_test.jsonl'),open('root_entity_dev.txt')):
	line1 = line1.strip()
	line2 = line2.strip()
	line3 = line3.strip()
  line4 = line3.strip()
	google = ast.literal_eval(line1)
	ner = ast.literal_eval(line2)
  root = ast.literal_eval(line4)
	
  combined = []
	c = 1
	if len(google)>0:
		for i in range(len(google)):
			if c>2:
				break
		
			if 'disambiguation' not in google[i] and 'List_of' not in google[i] and 'discography' not in google[i]:
				combined.append(google[i])
				c = c+1
	
	c=1
	
	for elem in ner:
		if c>2:
			break
		if elem not in combined and ('disambiguation' not in elem and 'List_of' not in elem and 'discography' not in elem):
			combined.append(elem)
			c = c+1
	
	
  for elem in root:
		if elem not in combined and ('disambiguation' not in elem and 'List_of' not in elem and 'discography' not in elem):
			combined.append(elem)
			c = c+1
	
	m[coun] = combined
	size = size + len(combined)
	coun = coun+1

count = 1


#this will your new file with all the retrived documents which you will use for sentence selection


f = open('dev_new5.jsonl','w')
for line in open('/Users/tuhinchakrabarty/Desktop/shared_task_dev.jsonl','r'):
	line = json.loads(line)
	line['predicted_pages'] = m[count]
	f.write(json.dumps(line)+'\n')
	count = count+1













