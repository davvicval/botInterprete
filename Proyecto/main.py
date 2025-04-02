import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen (puedes restringirlo si lo deseas)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el dataset
df = pd.read_csv("universidad_sevilla.csv")  # Asegúrate de que el CSV está en la misma carpeta

def buscar_info(consulta):
    consulta = consulta.lower()
    
    # Buscar coincidencias en la columna "Palabras Clave"
    resultados = df[df["Palabras Clave"].str.contains(consulta, case=False, na=False)]

    if resultados.empty:
        return {"respuesta": "No encontré información relevante. Prueba con otras palabras."}

    # Devolver los resultados con sus enlaces
    respuesta = [{"categoría": row["Categoría"], "descripción": row["Descripción"], "url": row["URL"]} for _, row in resultados.iterrows()]
    
    return {"resultados": respuesta}

@app.get("/buscar/")
def buscar(consulta: str = Query(..., title="Consulta")):
    return buscar_info(consulta)
