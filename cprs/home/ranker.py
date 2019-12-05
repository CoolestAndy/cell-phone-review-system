from collections import Counter
import nltk
from tqdm import tqdm
from spellchecker import SpellChecker

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class Tokenizer:
    wnl = nltk.stem.WordNetLemmatizer()
    spell = SpellChecker()

    def tokenize_batch(self, documents: [str]):
        print('Tokenizing...')
        tokens = [nltk.word_tokenize(document.lower()) for document in tqdm(documents)]
        print('Analyzing pos tags...')
        pos_tags = nltk.pos_tag_sents(tqdm(tokens))
        print('Lemmatizing...')
        return [
            [self.wnl.lemmatize(word, tag[0].lower()) if tag[0].lower() in {'a', 'r', 'n', 'v'} else word
             for word, tag in pos_tag]
            for pos_tag in tqdm(pos_tags)
        ]

    def tokenize(self, document: str, fuzzy=False):
        tokens = nltk.word_tokenize(document.lower())
        tokens = [
            self.wnl.lemmatize(word, tag[0].lower()) if tag[0].lower() in {'a', 'r', 'n', 'v'} else word
            for word, tag in nltk.pos_tag(tokens)
        ]
        if fuzzy:
            tokens = [self.spell.correction(token) for token in tokens]
        return tokens


class Ranker:
    def __init__(self, k1=0.5, k2=0.35):
        self.k1 = k1
        self.k2 = k2
        self.tokenizer = Tokenizer()

    def make_inverted_index(self, documents: [str], document_ids: [str]):
        document_terms = self.tokenizer.tokenize_batch(documents)
        self.doc_term_count = {
            document_ids[i]: Counter(terms)
            for i, terms in enumerate(document_terms)
        }
        self.doc_count = Counter()
        for terms in document_terms:
            for term in set(terms):
                self.doc_count[term] += 1
        self.doc_size = {
            document_ids[i]: len(terms)
            for i, terms in enumerate(document_terms)
        }
        self.total_dl = sum(len(document) for document in documents)
        self.num_docs = len(documents)

    def add_document(self, document: str, document_id: str):
        terms = self.tokenizer.tokenize(document)
        self.doc_term_count[document_id] = Counter(terms)
        for term in set(terms):
            self.doc_count[term] += 1
        self.doc_size[document_id] = len(terms)
        self.total_dl += len(document)
        self.num_docs += 1

    def remove_document(self, document: str, document_id: str):
        terms = self.tokenizer.tokenize(document)
        del self.doc_term_count[document_id]
        for term in set(terms):
            self.doc_count[term] -= 1
        del self.doc_size[document_id]
        self.total_dl -= len(document)
        self.num_docs -= 1

    def score(self, document_id: str, query: str):
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
        query = self.tokenizer.tokenize(query, fuzzy=True)
        doc_term_count = sum(self.doc_term_count[document_id][term] for term in query)
        doc_size = self.doc_size[document_id]
        doc_count = sum(self.doc_count[term] for term in query)
        avg_dl = self.total_dl / self.num_docs
        query_term_weight = len(query)

        TF = doc_term_count / (doc_term_count + 0.5 + self.k1 * doc_size / avg_dl)
        IDF = (self.num_docs / doc_count) ** self.k2 if doc_count > 0 else 0
        return TF * IDF * query_term_weight
