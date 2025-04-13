import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_md")

# Cargar el dataset
df = pd.read_csv("universidad_sevilla_mod.csv")

# Crear el vectorizador de TF-IDF para las palabras clave
vectorizer = TfidfVectorizer(stop_words='english')

# Vectorizamos solo la columna "Palabras Clave"
X = vectorizer.fit_transform(df["Palabras Clave"].fillna(""))  # Rellenar NaN por si acaso

# Función para obtener sinónimos automáticos utilizando spaCy
def obtener_sinonimos(palabra):
    # Procesar la palabra usando spaCy
    doc = nlp(palabra)
    sinonimos = set()

    # Usamos las entidades del vocabulario de spaCy para encontrar términos similares
    for token in doc:
        for similar_token in token.vocab:
            if token.is_stop or similar_token.is_stop:
                continue  # Ignorar stopwords
            if token.text != similar_token.text and similar_token.vector.any():
                similitud = token.similarity(similar_token)
                if similitud > 0.7:  # Umbral para considerar un sinónimo
                    sinonimos.add(similar_token.text)

    return list(sinonimos)

# Función para enriquecer la consulta automáticamente
def enriquecer_consulta(consulta):
    consulta = consulta.lower()
    palabras = consulta.split()

    # Agregar los sinónimos automáticamente
    consulta_enriquecida = set(palabras)  # Comenzamos con las palabras originales

    for palabra in palabras:
        # Obtener sinónimos automáticos
        sinonimos = obtener_sinonimos(palabra)
        consulta_enriquecida.update(sinonimos)

    return " ".join(consulta_enriquecida)

# Función para realizar la búsqueda
def buscar_info(consulta):
    consulta_enriquecida = enriquecer_consulta(consulta)

    consulta_vector = vectorizer.transform([consulta_enriquecida])
    similitudes = cosine_similarity(consulta_vector, X).flatten()

    # Obtener los índices ordenados por similitud (top 2 en lugar de 1)
    indices_top = similitudes.argsort()[-2:][::-1]  # Obtenemos los dos índices más similares

    # Lista para almacenar los resultados
    resultados = []

    for idx in indices_top:
        mejor_coincidencia = df.iloc[idx]
        categoria = mejor_coincidencia["Categoría"]
        sim = similitudes[idx]

        # Verificamos si la URL está vacía
        url = mejor_coincidencia["URL"] if pd.notna(mejor_coincidencia["URL"]) else categoria

        # Si la similitud es mayor que el umbral (ajustable)
        if sim > 0.2:
            resultados.append({
                "categoría": categoria,
                "descripción": mejor_coincidencia["Descripción"],
                "url": url
            })

    # Si se encontró alguna coincidencia relevante
    if resultados:
        return {
            "respuesta": "Encontré información relacionada con tu consulta.",
            "resultados": resultados
        }
    else:
        return {"respuesta": "No encontré información relevante. Prueba con otras palabras."}

# Configuración de FastAPI
app = FastAPI()

# Habilitar CORS para el frontend
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



