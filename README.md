# Bot Intérprete de Peticiones sobre la Universidad de Sevilla
Este proyecto es un bot web que interpreta consultas escritas en lenguaje natural sobre distintos recursos de la Universidad de Sevilla y devuelve enlaces útiles relacionados con la información buscada.

---

## ¿Cómo arrancar la aplicación?

1. Asegúrese de tener instalada **una versión de Python** (3.x) y **pip**.  
   Si pip no está instalado, ejecute:

   ```bash
   python -m ensurepip --default-pip
2. Abra una terminal en Visual Studio Code en la carpeta del proyecto.
3. Instale las dependencias necesarias con los siguientes comandos:
    ```bash
    pip install fastapi uvicorn pandas
    pip install scikit-learn       # Para el árbol de decisión
    pip install spacy              # Para el análisis de texto
    python -m spacy download es_core_news_md
4. Arranque el servidor FastAPI con:
    ```bash
    uvicorn main:app --reload
5. Abra el archivo index.html en su navegador para comenzar a usar el bot.

## ¿Cómo funciona el bot?

1. El usuario escribe una consulta en lenguaje natural en la interfaz web.
2. El texto es procesado para detectar sinónimos automáticamente mediante el modelo en español de spaCy.
3. Se crea un vector numérico TF-IDF de la consulta enriquecida y se compara con los recursos del dataset.
4. Se calcula la similitud de coseno entre la consulta y las entradas del dataset.
5. Se devuelven los resultados más relevantes, incluyendo descripción, categoría y enlace directo.

## Estructura del proyecto

- **main.py**: Backend de la aplicación (FastAPI).
- **universidad_sevilla.csv**: Dataset con recursos y enlaces de la Universidad de Sevilla.
- **index.html**: Interfaz web del usuario.
- **README.md**: Documento con instrucciones y guía del proyecto.

## Requisitos previos

- Python 3.7 o superior.
- pip instalado y funcionando.
- Navegador moderno para abrir la interfaz.
- Conexión a internet para descargar el modelo de spaCy (es_core_news_md).

## Autores
Este bot fue desarrollado por Isabel Sánchez Castro y David Vicente Valderrama como proyecto para la asignatura Complementos de Bases de Datos.