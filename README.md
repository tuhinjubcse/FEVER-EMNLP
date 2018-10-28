# FEVER-EMNLP
This repository contains the code for COLUMBIA NLP's submission to FEVER (Fact Extraction and Verification Workshop) ,EMNLP 2018

getCombinedDoc.py gives u the combination of documents retrived from all methods google search / NER / root entity before first VP

src/retrieval/top_n.py does sentence selection and stores top 5 sentences based on tf idf similarity to a text file
