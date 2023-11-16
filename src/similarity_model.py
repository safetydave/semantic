import numpy as np
import tensorflow_hub as hub
from gensim.models import KeyedVectors
from numpy.linalg import norm


class SimilarityModelW2V:

    def __init__(self, base_vocabulary, semantics=None):
        self.description = 'w2v'
        self.semantics = semantics
        if self.semantics is None:
            model = "../data/GoogleNews-vectors-negative300.bin"
            self.semantics = KeyedVectors.load_word2vec_format(model, binary=True)
        self.vocab_words = [w for w in base_vocabulary.words if w in self.semantics]
        self.embeddings = np.array([self.semantics[w] for w in self.vocab_words])

    def word_string(self, index):
        return self.vocab_words[index]

    def word_index(self, string):
        return self.vocab_words.index(string)

    def word_embedding(self, index):
        return self.embeddings[index]

    def random_guesses(self, n):
        return np.random.randint(len(self.vocab_words), size=n)

    def similarities(self, embedding):
        return self.semantics.cosine_similarities(embedding, self.embeddings)


def np_cosine(e, es):
    return np.dot(es, e) / (norm(es, axis=1) * norm(e))


class SimilarityModelUSE:

    def __init__(self, base_vocabulary):
        self.description = 'USE'
        use_ref = "https://tfhub.dev/google/universal-sentence-encoder/4"
        self.semantics = hub.load(use_ref)
        self.vocab_words = np.array(base_vocabulary.words)
        self.embeddings = self.semantics(self.vocab_words).numpy()

    def word_string(self, index):
        return self.vocab_words[index]

    def word_index(self, string):
        return np.nonzero(self.vocab_words == string)[0][0]

    def word_embedding(self, index):
        return self.embeddings[index]

    def random_guesses(self, n):
        return np.random.randint(len(self.vocab_words), size=n)

    def similarities(self, embedding):
        return np_cosine(embedding, self.embeddings)
