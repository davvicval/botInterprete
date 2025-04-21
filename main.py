import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_md")

# Cargar el dataset
df = pd.read_csv("universidad_sevilla.csv")

# Crear el vectorizador de TF-IDF para las palabras clave
spanish_stopwords = list(nlp.Defaults.stop_words)
vectorizer = TfidfVectorizer(stop_words=spanish_stopwords)

# Vectorizamos solo la columna "Palabras Clave"
X = vectorizer.fit_transform(df["Palabras Clave"].fillna(""))  # Rellenar NaN por si acaso

# Función para obtener sinónimos automáticos utilizando spaCy
def obtener_sinonimos(palabra):

    doc = nlp(palabra)
    sinonimos = set()

    for token in doc:
        for similar_token in token.vocab:
            if token.is_stop or similar_token.is_stop:
                continue
            if token.text != similar_token.text and similar_token.vector.any():
                similitud = token.similarity(similar_token)
                if similitud > 0.7:
                    sinonimos.add(similar_token.text)

    return list(sinonimos)

# Función para enriquecer la consulta automáticamente
def enriquecer_consulta(consulta):
    consulta = consulta.lower()
    palabras = consulta.split()
    consulta_enriquecida = set(palabras)

    for palabra in palabras:
        sinonimos = obtener_sinonimos(palabra)
        consulta_enriquecida.update(sinonimos)

    return " ".join(consulta_enriquecida)

# Función para realizar la búsqueda
def buscar_info(consulta):
    consulta_enriquecida = enriquecer_consulta(consulta)

    consulta_vector = vectorizer.transform([consulta_enriquecida])
    similitudes = cosine_similarity(consulta_vector, X).flatten()

    indices_top = similitudes.argsort()[-2:][::-1]

    resultados = []

    for idx in indices_top:
        mejor_coincidencia = df.iloc[idx]
        categoria = mejor_coincidencia["Categoría"]
        sim = similitudes[idx]

        url = mejor_coincidencia["URL"] if pd.notna(mejor_coincidencia["URL"]) else categoria

        if sim > 0.2:
            resultados.append({
                "categoría": categoria,
                "descripción": mejor_coincidencia["Descripción"],
                "url": url
            })

    if resultados:
        return {
            "respuesta": "Encontré información relacionada con tu consulta.",
            "resultados": resultados
        }
    else:
        return {"respuesta": "No encontré información relevante. Prueba con otras palabras."}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/buscar/")
def buscar(consulta: str = Query(..., title="Consulta")):
    return buscar_info(consulta)

@app.get("/")
def inicio():
    return {"mensaje": "Bot de la Universidad de Sevilla activo. Usa /buscar/?consulta=... para hacer una búsqueda."}