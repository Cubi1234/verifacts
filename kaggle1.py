import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

#Read the data
df=pd.read_csv('fake_or_real_news.csv')

#Get shape and head
df.shape
df.head()

labels=df.label
labels.head()

x_train,x_test,y_train,y_test=train_test_split(df['text'], labels, test_size=0.2, random_state=7)
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df =0.9)
## DataFlair - fit and transform train set, transform test set
tfidf_train = tfidf_vectorizer.fit_transform(x_train)
tfidf_test = tfidf_vectorizer.transform(x_test)

pac=PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train,y_train)

#DataFlair - Predict on the test set and calculate accuracy
y_pred=pac.predict(tfidf_test)
score=accuracy_score(y_test,y_pred)
print(f'Accuracy: {round(score*100,2)}%')
print(confusion_matrix(y_test,y_pred, labels=['FAKE','REAL']))

while True:
    titular_noticia = input("Ingresa un titular de noticia falsa (o escribe 'salir' para terminar): ")
    if titular_noticia.lower() == 'salir':
        print("¡Hasta luego!")
        break
    titular_vectorizado = tfidf_vectorizer.transform([titular_noticia])
    prediccion = pac.predict(titular_vectorizado)
    print("Predicción:", prediccion[0])