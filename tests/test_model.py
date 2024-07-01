import unittest
import requests
from modelo import preprocess, classifier, vectorizer

class TestModelPredictions(unittest.TestCase):

    def test_prediction(self):
        # Ejemplos de titulares de prueba
        headlines = [
            "The Expert Trick They Don't Want You to Know About Making Money from Home",
            "Sabrina the Teenage Witch star Martin Mull dies at 80",
            "The Biggest Mistake You Make Every Day and How to Easily Fix It",
            "Serbian officer shot with crossbow outside Israeli embassy"
        ]

        expected_predictions = [
            1,  # Clickbait
            0,  # No clickbait
            1,  # Clickbait
            0   # No clickbait
        ]

        for headline, expected in zip(headlines, expected_predictions):
            processed_headline = preprocess(headline)
            vect_headline = vectorizer.transform([processed_headline])
            prediction = classifier.predict(vect_headline)[0]
            self.assertEqual(prediction, expected, f"Para el titular '{headline}', se esperaba '{expected}' pero se obtuvo '{prediction}'")

if __name__ == '__main__':
    unittest.main()
