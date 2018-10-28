import json
from drqa import retriever
import ast
from time import sleep
from googleapiclient.discovery import build
import pprint


#USE YOUR OWN KEY

my_api_key = "AIzaSyBzbRQVQ9V1H4l9iQbJQj6w4xvoic4Yb_c"
my_cse_id = "000482614213441882806:lyzkmjblegi"



print('Finished Populating')

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    if 'items' in res:
    	return res['items']
    else:
    	return []



c = 0
a = ['blind_task_test.jsonl']  #change name of file for dev set 
f1 = open('blind_test_google.txt','a') #again file name can be changed
for file in a:
	f = open(file,'r')
	count = 1
	for line in f:
		line = json.loads(line.strip())
		count = count+1
		claim = line['claim'][:-1]+ ' .'
		results = google_search('wikipedia '+claim, my_api_key, my_cse_id, num=5)
		res = []
		c = 0
		for result in results:
			if 'https://en.wikipedia.org/wiki/' in result['formattedUrl'] and c<3:
				b = result['formattedUrl'].replace('https://en.wikipedia.org/wiki/','')
				c = c+1
				b = b.replace('(','-LRB-')
				b = b.replace(')','-RRB-')
				b = b.replace(':','-COLON-')
				b = b.replace('%26','&')
				b = b.replace('%27',"'")
				b = b.replace('%22','"')
				b = b.replace('%3F','?')
				res.append(b)
		f1.write(claim+'\t'+json.dumps(res)+'\n')
		


