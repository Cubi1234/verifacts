import requests
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
from google.oauth2 import service_account
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
CORS(app)
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

DB_NAME = 'verifacts'
DB_USER = 'mtis'
DB_PASSWORD = 'new_password'
DB_HOST = 'localhost'
DB_PORT = '3306'

# Cargar el dataset
data = pd.read_csv('clickbait_data.csv')

# Dividir el dataset en sets de entrenamiento y pruebas
X = data['headline']
y = data['clickbait']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=22, stratify=y)

# Funciones de preprocesamiento del texto
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

# Preprocesar los datos de entrenamiento y prueba
X_train = X_train.apply(preprocess)
X_test = X_test.apply(preprocess)

# Vectorizar los datos
vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2), max_features=22500)
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Clasificador Naive Bayes Multinomial
classifier = MultinomialNB()
classifier.fit(X_train_vect, y_train)

# Evaluar el modelo
y_pred = classifier.predict(X_test_vect)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)

# Visualizar la matriz de confusión
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-clickbait', 'Clickbait'], yticklabels=['Non-clickbait', 'Clickbait'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Función de clasificación de titulares
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

@app.route('/fact_check', methods=['GET'])
def fact_check():
    # API endpoint
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    # Query parameters
    query = request.args.get('query')
    language_code = request.args.get('languageCode')
    review_publisher_site_filter = request.args.get('reviewPublisherSiteFilter')
    max_age_days = request.args.get('maxAgeDays')
    page_size = request.args.get('pageSize')
    page_token = request.args.get('pageToken')
    offset = request.args.get('offset')

    params = {
        'query': query,
        'languageCode': language_code,
        'reviewPublisherSiteFilter': review_publisher_site_filter,
        'maxAgeDays': max_age_days,
        'pageSize': page_size,
        'pageToken': page_token,
        'offset': offset,
        'key': 'XXX'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
