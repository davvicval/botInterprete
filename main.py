import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_md")

# Configurar CORS para permitir peticiones desde el frontend
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el dataset
df = pd.read_csv("universidad_sevilla.csv")

# Crear el vectorizador de TF-IDF para palabras clave y categorías
vectorizer = TfidfVectorizer(stop_words='english')  # Ignorar palabras vacías

# Combinamos las columnas "Palabras Clave" y "Categoría" en una sola lista para el vectorizador
df_combined = df["Palabras Clave"] + " " + df["Categoría"]  # Concatenamos palabras clave y categoría

# Ajustamos el vectorizador para trabajar con ambas columnas combinadas
X_combined = vectorizer.fit_transform(df_combined.fillna(""))  # Rellenar NaN por si acaso

# Función para obtener sinónimos de una palabra utilizando spaCy
def obtener_sinonimos(palabra):
    doc = nlp(palabra)
    sinonimos = set()

    # Buscamos sinónimos de las palabras en la consulta utilizando el modelo de spaCy
    for token in doc:
        for syn in token.vocab.vectors:
            if syn in token.vocab.vectors:
                sinonimos.add(token.text)
    return list(sinonimos)

# Función de búsqueda con sinónimos
def buscar_info(consulta):
    consulta = consulta.lower()

    # Obtén sinónimos de cada palabra en la consulta
    palabras = consulta.split()
    palabras_con_sinonimos = set(palabras)  # Comenzamos con las palabras originales

    for palabra in palabras:
        sinonimos = obtener_sinonimos(palabra)
        palabras_con_sinonimos.update(sinonimos)

    # Concatenamos todas las palabras con sinónimos para hacer la búsqueda
    consulta_enriquecida = " ".join(palabras_con_sinonimos)

    # Vectorizamos la consulta enriquecida
    consulta_vector = vectorizer.transform([consulta_enriquecida])

    # Calcular similitud coseno entre la consulta enriquecida y la combinación de palabras clave y categorías
    similitudes = cosine_similarity(consulta_vector, X_combined).flatten()

    # Obtener el índice de la fila con la mayor similitud
    mejor_coincidencia_idx = similitudes.argmax()

    # Obtener la fila correspondiente con la mayor similitud
    mejor_coincidencia = df.iloc[mejor_coincidencia_idx]

    # Verificar si la similitud es lo suficientemente alta
    if similitudes[mejor_coincidencia_idx] > 0.4:  # Umbral de similitud (ajustable)
        # Acceder correctamente a la fila de datos
        categoria = mejor_coincidencia["Categoría"]
        descripcion = mejor_coincidencia["Descripción"]
        url = mejor_coincidencia["URL"]
        
        # Devolver la respuesta correcta
        return {
            "respuesta": f"Encontré algo relacionado con tu consulta.",
            "resultados": [{
                "categoría": categoria,
                "descripción": descripcion,
                "url": url
            }]
        }
    else:
        return {"respuesta": "No encontré información relevante. Prueba con otras palabras."}

@app.get("/buscar/")
def buscar(consulta: str = Query(..., title="Consulta")):
    return buscar_info(consulta)

@app.get("/")
def inicio():
    return {"mensaje": "Bot de la Universidad de Sevilla activo. Usa /buscar/?consulta=... para hacer una búsqueda."}




