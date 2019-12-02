from collections import Counter
import nltk

class Ranker:
    def __init__(self, k1=0.5, k2=0.35):
        self.k1 = k1
        self.k2 = k2

    def make_inverted_index(self, documents: [str]):
        document_terms = [nltk.word_tokenize(document.lower()) for document in documents]
        self.doc_term_count = [Counter(terms) for terms in document_terms]
        self.doc_count = Counter()
        for terms in document_terms:
            for term in set(terms):
                self.doc_count[term] += 1
        self.doc_size = [len(terms) for terms in document_terms]
        self.avg_dl = sum(len(document) for document in documents) / len(documents)
        self.num_docs = len(documents)

    def score(self, document_idx: int, query: str):
        """
        You need to override this function to return a score for a single term.

        You may want to call some of the following variables when implementing your retrieval function:
        sd.avg_dl: average document length of the collection
        sd.num_docs: total number of documents in the index
        sd.total_terms: total number of terms in the index
        sd.query_length: the total length of the current query (sum of all term weights)
        sd.query_term_weight: query term count (or weight in case of feedback)
        sd.doc_count: number of documents that a term t_id appears in
        sd.corpus_term_count: number of times a term t_id appears in the collection
        sd.doc_term_count: number of times the term appears in the current document
        sd.doc_size: total number of terms in the current document
        sd.doc_unique_terms: number of unique terms in the current document
        """
        query = nltk.word_tokenize(query.lower())
        doc_term_count = sum(self.doc_term_count[document_idx][term] for term in query)
        doc_size = self.doc_size[document_idx]
        doc_count = sum(self.doc_count[term] for term in query)
        query_term_weight = len(query)

        TF = doc_term_count / (doc_term_count + 0.5 + self.k1 * doc_size / self.avg_dl)
        IDF = (self.num_docs / doc_count) ** self.k2 if doc_count > 0 else 0
        return TF * IDF * query_term_weight
