from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import re
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Download necessary NLTK resources
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

DB_NAME = 'verifacts'
DB_USER = 'mtis'
DB_PASSWORD = 'new_password'
DB_HOST = 'localhost'
DB_PORT = '3306'

# Load the dataset
data = pd.read_csv('clickbait_data.csv')

# Split the dataset into training and testing sets
X = data['headline']
y = data['clickbait']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=22, stratify=y)

# Define text preprocessing functions
def tokenize(text):
    return text.split()

def to_lowercase(tokens):
    return [token.lower() for token in tokens]

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

def remove_punctuation(tokens):
    return [re.sub(f'[{string.punctuation}]', '', token) for token in tokens]

def remove_digits(tokens):
    return [re.sub(r'\d+', '', token) for token in tokens]

def remove_whitespace(tokens):
    return [token.strip() for token in tokens]

def lemmatize(tokens):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def preprocess(text):
    tokens = tokenize(text)
    tokens = to_lowercase(tokens)
    tokens = remove_stopwords(tokens)
    tokens = remove_punctuation(tokens)
    tokens = remove_digits(tokens)
    tokens = remove_whitespace(tokens)
    tokens = lemmatize(tokens)
    return ' '.join(tokens)

# Preprocess the training data
X_train = X_train.apply(preprocess)

# Vectorize the text data
vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2), max_features=22500)
X_train_vect = vectorizer.fit_transform(X_train)

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train_vect, y_train)

# Function to classify a headline
def classify_headline(headline):
    processed_headline = preprocess(headline)
    vect_headline = vectorizer.transform([processed_headline])
    prediction = classifier.predict(vect_headline)
    probability_scores = classifier.predict_proba(vect_headline)[0]
    certainty = max(probability_scores)
    result = 'Clickbait' if prediction[0] == 1 else 'Non-clickbait'
    return result, certainty


# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    headline = data['headline']
    result, certainty = classify_headline(headline)
    
    # Store prediction in the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO verifacts.predicciones (titular, prediccion, certeza) VALUES (%s, %s, %s)", (headline, result, certainty))
            conn.commit()
    
    return jsonify({"result": result, "certainty": certainty})

@app.route('/all_entries', methods=['GET'])
def get_all_entries():
    # Connect to the database
    conn = get_db_connection()
    cur = conn.cursor()

    # Query all entries in the 'predicciones' table
    cur.execute("SELECT * FROM predicciones ORDER BY fecha_hora DESC LIMIT 50")
    entries = cur.fetchall()

    # Close the database connection
    cur.close()
    conn.close()

    # Return entries as JSON response
    return jsonify(entries)

if __name__ == '__main__':
    app.run(debug=True)
