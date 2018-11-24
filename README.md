# FEVER-EMNLP
This repository contains the code for COLUMBIA NLP's submission to FEVER (Fact Extraction and Verification Workshop) ,EMNLP 2018 from our paper (https://aclanthology.info/papers/W18-5521/w18-5521)
 Robust Document Retrieval and Individual Evidence Modeling for Fact Extraction and Verification.
 
 If you find the code useful or use it please dont forget to cite .
 
 @InProceedings{W18-5521,
  author = 	"Chakrabarty, Tuhin
		and Alhindi, Tariq
		and Muresan, Smaranda",
  title = 	"Robust Document Retrieval and Individual Evidence Modeling for Fact Extraction and Verification.",
  booktitle = 	"Proceedings of the First Workshop on Fact Extraction and VERification (FEVER)",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"127--131",
  location = 	"Brussels, Belgium",
  url = 	"http://aclweb.org/anthology/W18-5521"
}

*Doc Retrival*

getCombinedDoc.py gives u the combination of documents retrived from all methods google search / NER / root entity before first VP


*Sentence Selection*

src/retrieval/top_n.py does sentence selection and stores top 5 sentences based on tf idf similarity to a text file

sentencefilter.py takes the text file as input produced by file (src/retrieval/top_n.py) . Selected top 5 sentences based on  tfidf cosine similarity  are further converted to vectors using  elmo embedding and top 3 out of 5 are passed to entailment model based on semantic similarity to claim


*Textual Entailment*

It produces files s1.dev , s2.dev , labels.dev for dev file , s1.test , s2.test , labels.test for test file
s1.train , s2.train , labels.train for train file

These files are to be used for Textual Entailment

Create folder dataset/ols/SNLI and put all these files there
beacuse fastText and pytorch had a version problem . run train_nli once it creates the word_dict.txt file and then stop it .
getFastText.py creates embedding.txt in same directory from word_dict.txt , once it is done
run train_nli and you are good


After finishing the running it produces predictions for test and train .
Use majority.py to get single entailment prediction from multiple evidences using our algorithm 


