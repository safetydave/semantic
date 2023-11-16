import unittest

from src.vocabulary import VocabularyEWS, VocabularyUF


class TestVocabulary(unittest.TestCase):

    def test_vocabulary_size_should_be_human_typical(self):
        v_ews = VocabularyEWS()
        self.assertGreaterEqual(len(v_ews.words), 25000)
        self.assertLessEqual(len(v_ews.words), 30000)
        v_uf = VocabularyUF()
        self.assertGreaterEqual(len(v_uf.words), 25000)
        self.assertLessEqual(len(v_uf.words), 30000)

    def test_nsfw_words_should_be_removed(self):
        v_uf = VocabularyUF()
        self.assertIn('ass', v_uf.words)
        v_uf.remove_nsfw_words()
        self.assertNotIn('ass', v_uf.words)


if __name__ == '__main__':
    unittest.main()
