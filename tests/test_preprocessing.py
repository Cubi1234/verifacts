import unittest
from modelo import tokenize, to_lowercase, remove_stopwords, remove_punctuation, remove_digits, remove_whitespace, lemmatize

class TestPreprocessing(unittest.TestCase):

    def test_tokenization(self):
        text = "This is a test headline."
        expected = ["This", "is", "a", "test", "headline."]
        self.assertEqual(tokenize(text), expected)
        text = "Este truco simple te ayudará a duplicar tu productividad"
        expected = ["Este", "truco", "simple", "te", "ayudará", "a", "duplicar", "tu", "productividad"]
        self.assertEqual(tokenize(text), expected)

    def test_to_lowercase(self):
        tokens = ["This", "Is", "A", "Test"]
        expected = ["this", "is", "a", "test"]
        self.assertEqual(to_lowercase(tokens), expected)
        tokens = ["Este", "TrUco", "SIMPLE", "te", "ayUDArá", "a", "DUplicar", "tu", "pRODuctividad"]
        expected = ["este", "truco", "simple", "te", "ayudará", "a", "duplicar", "tu", "productividad"]
        self.assertEqual(to_lowercase(tokens), expected)

    def test_remove_stopwords(self):
        tokens = ["this", "is", "a", "test"]
        expected = ["test"]
        self.assertEqual(remove_stopwords(tokens), expected)

    def test_remove_punctuation(self):
        tokens = ["this,", "is.", "a!", "test"]
        expected = ["this", "is", "a", "test"]
        self.assertEqual(remove_punctuation(tokens), expected)

    def test_remove_digits(self):
        tokens = ["test1", "headline2"]
        expected = ["test", "headline"]
        self.assertEqual(remove_digits(tokens), expected)

    def test_remove_whitespace(self):
        tokens = [" test ", " headline "]
        expected = ["test", "headline"]
        self.assertEqual(remove_whitespace(tokens), expected)

if __name__ == '__main__':
    unittest.main()
