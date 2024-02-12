import spacy
import pandas as pd

# Cargar el modelo preentrenado
nlp = spacy.load("en_core_web_lg")

# Leer el conjunto de datos de noticias desde un archivo CSV
data = pd.read_csv("fake_or_real_news.csv")

# Obtener los titulares de las noticias y las etiquetas del conjunto de datos
titulares_noticias = data["title"]
etiquetas = data["label"]

# Contar el número de titulares en el conjunto de datos
numero_titulares = len(titulares_noticias)


# Procesar cada titular de noticia con SpaCy y su etiqueta correspondiente
for titulo_noticia, etiqueta in zip(titulares_noticias, etiquetas):
    doc = nlp(titulo_noticia)
    print("Número de titulares en el CSV:", numero_titulares)
    # Imprimir la etiqueta de la noticia
    print("\nEtiqueta:", etiqueta)
    
    # Imprimir las entidades nombradas detectadas en el titular
    print("Entidades nombradas:")
    for ent in doc.ents:
        print(ent.text, "-", ent.label_)

    # Imprimir las palabras y su lema en el titular
    print("\nPalabra - Lema:")
    for token in doc:
        print(token.text, "-", token.lemma_)
    print("---------------------------------------------------")
