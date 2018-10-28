import math
import json
from .retrieval_method import RetrievalMethod
from drqa import retriever
from drqascripts.retriever.build_tfidf_lines import OnlineTfidfDocRanker
from nltk.corpus import stopwords
import unicodedata
stop_words = set(stopwords.words('english'))
fil = open('/Users/tuhinchakrabarty/Desktop/FEVER/fever-baselines/document_shared_dev.txt','w')



class TopNDocsTopNSents(RetrievalMethod):

    class RankArgs:
        def __init__(self):
            self.ngram = 2
            self.hash_size = int(math.pow(2,24))
            self.tokenizer = "simple"
            self.num_workers = None

    def __init__(self,db,n_docs,n_sents,model):
        super().__init__(db)
        self.n_docs = n_docs
        self.n_sents = n_sents
        self.ranker = retriever.get_class('tfidf')(tfidf_path=model)
        self.onlineranker_args = self.RankArgs()

    def get_docs_for_claim(self, claim_text):
        doc_names, doc_scores = self.ranker.closest_docs(claim_text, self.n_docs)
        return zip(doc_names, doc_scores)


    def tf_idf_sim(self, claim, lines, freqs=None):
        tfidf = OnlineTfidfDocRanker(self.onlineranker_args, [line["sentence"] for line in lines], freqs)
        line_ids, scores = tfidf.closest_docs(claim,self.n_sents)
        ret_lines = []
        for idx, line in enumerate(line_ids):
            ret_lines.append(lines[line])
            ret_lines[-1]["score"] = scores[idx]

        ret_lines = list(sorted(ret_lines,  key=lambda elem: (-elem['score'],elem['page'] ,elem['line_on_page'])))
        a = {}
        a['claim'] = claim
        a['sentences'] = ret_lines
        fil.write(json.dumps(a)+'\n')
        return ret_lines[0:5]



    def get_sentences_for_claim(self,line,include_text=False):

        pages = list(line['predicted_pages'])
        print(pages)
        p_lines = []
        for page in pages:
            lines = self.db.get_doc_lines(page)
            if lines!=None:
                lines = [line.split("\t")[1] if len(line.split("\t"))>1 and len(line.split("\t")[1]) > 1 else "" for line in
                     lines.split("\n")]

                p_lines.extend(zip(lines, [page] * len(lines), range(len(lines))))


        lines = []
        for p_line in p_lines:
            lines.append({
                "sentence": p_line[0],
                "page": p_line[1],
                "line_on_page": p_line[2]
            })

        scores = self.tf_idf_sim(line['claim'], lines)

        if include_text:
            return scores

        return [(s["page"], s["line_on_page"]) for s in scores]
