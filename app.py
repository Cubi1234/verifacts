from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import nltk

app = Flask(__name__)
CORS(app)

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

data = pd.read_csv("fake_or_real_news.csv")
real_news_additional_data = pd.read_csv("True.csv")
real_news_additional_data['label'] = 'REAL'
fake_news_additional_data = pd.read_csv("Fake.csv")
fake_news_additional_data['label'] = 'FAKE'
data = pd.concat([data, real_news_additional_data, fake_news_additional_data], ignore_index=True)
data['title'] = data['title'].apply(preprocess_text)

X = data['title']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_vectorized, y_train)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    headline = data['headline']
    preprocessed_headline = preprocess_text(headline)
    headline_vectorized = vectorizer.transform([preprocessed_headline])
    prediction = rf_classifier.predict(headline_vectorized)
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
