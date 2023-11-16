from english_words import english_words_set
import pandas as pd
from urllib.request import urlopen

# size of english_words_set
BASE_VOCABULARY_SIZE = 25487

# List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words
NSFW_WORDS = 'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en'


class Vocabulary:

    def __init__(self):
        self.words = None

    def add(self, word):
        self.words.append(word)

    def add_missing_words(self, words):
        added = []
        for w in words:
            if w not in self.words:
                self.add(w)
                added.append(w)
        return added

    def remove_nsfw_words(self):
        count = 0
        for line in urlopen(NSFW_WORDS):
            nsfw_word = line.decode()[:-1]
            if nsfw_word in self.words:
                self.words.remove(nsfw_word)
                count = count + 1
        return count


class VocabularyEWS(Vocabulary):

    def __init__(self):
        Vocabulary.words = list(english_words_set)


class VocabularyUF(Vocabulary):

    def __init__(self):
        unigram_freq_df = pd.read_csv('../data/unigram_freq.csv').set_index('word')
        Vocabulary.words = list(unigram_freq_df.index[:BASE_VOCABULARY_SIZE])
        self.freqs = list(unigram_freq_df['count'][:BASE_VOCABULARY_SIZE])

    def add(self, word):
        Vocabulary.add(word)
        self.freqs.append(0)
