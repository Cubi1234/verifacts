import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Preprocessing function
def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Removing Punctuation and Special Characters
    tokens = [word for word in tokens if word.isalnum()]
    
    # Removing Stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    # Join the tokens back into a single string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

# Load the mixed dataset

# Load the additional real news dataset
real_news_additional_data = pd.read_csv("True.csv")
real_news_additional_data['label'] = 'REAL'

# Load the additional fake news dataset
fake_news_additional_data = pd.read_csv("Fake.csv")
fake_news_additional_data['label'] = 'FAKE'

# Concatenate the datasets
data = pd.concat([real_news_additional_data, fake_news_additional_data], ignore_index=True)

# Preprocess the 'title' column
data['title'] = data['title'].apply(preprocess_text)

# Split the data into features (titles) and labels (fake/real)
X = data['title']
y = data['label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a TF-IDF vectorizer to convert news headlines into numerical features
vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Initialize and train a Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_vectorized, y_train)

# Predict on the test set
y_pred = rf_classifier.predict(X_test_vectorized)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# Print classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Print confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(conf_matrix)

# Keep the program running to receive news headlines from the user
while True:
    news_headline = input("Enter a news headline (or type 'exit' to end): ")
    if news_headline.lower() == 'exit':
        print("Goodbye!")
        break
    preprocessed_headline = preprocess_text(news_headline)
    headline_vectorized = vectorizer.transform([preprocessed_headline])
    prediction = rf_classifier.predict(headline_vectorized)
    print("Prediction:", prediction[0])