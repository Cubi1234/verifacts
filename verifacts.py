import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Cargar el conjunto de datos mixto
data = pd.read_csv("fake_or_real_news.csv")

# Cargar el conjunto de datos de noticias reales 
real_news_additional_data = pd.read_csv("True.csv")
real_news_additional_data['label'] = 'REAL'

# Cargar el conjunto de datos de noticias falsas 
fake_news_additional_data = pd.read_csv("Fake.csv")
fake_news_additional_data['label'] = 'FAKE'

# Concatenar los tres conjuntos de datos
data = pd.concat([data, real_news_additional_data, fake_news_additional_data], ignore_index=True)

# Contar el número total de datos
numero_total_datos = len(data)
print("Número total de datos:", numero_total_datos)

# Dividir los datos en características (titulares) y etiquetas (fake/real)
X = data['title']
y = data['label']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Contar el número de datos en los conjuntos de entrenamiento y prueba
numero_datos_entrenamiento = len(X_train)
numero_datos_prueba = len(X_test)
print("Número de datos en el conjunto de entrenamiento:", numero_datos_entrenamiento)
print("Número de datos en el conjunto de prueba:", numero_datos_prueba)

# Crear un vectorizador TF-IDF para convertir los titulares de noticias en características numéricas
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Inicializar y entrenar un clasificador de Bosques Aleatorios
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_vectorized, y_train)

# Predecir en el conjunto de prueba
y_pred = rf_classifier.predict(X_test_vectorized)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print("Precisión del modelo:", accuracy)
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))
