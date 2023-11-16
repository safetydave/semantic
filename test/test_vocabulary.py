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

    def test_add_missing_words_should_add_to_vocabulary(self):
        v = VocabularyUF()
        vocab_length = len(v.words)
        missing_words = ['nononsense', 'nosensesense']
        v.add_missing_words(missing_words)
        self.assertEqual(len(v.words), vocab_length + len(missing_words))
        self.assertIn(missing_words[0], v.words)

    def test_nsfw_words_should_be_removed(self):
        v = VocabularyUF()
        self.assertIn('ass', v.words)
        v.remove_nsfw_words()
        self.assertNotIn('ass', v.words)


if __name__ == '__main__':
    unittest.main()
