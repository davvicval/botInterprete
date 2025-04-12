import pandas as pd

# Cargar el archivo CSV original
df = pd.read_csv("universidad_sevilla.csv")

# Palabras clave relevantes por categoría
palabras_clave_por_categoria = {
    "Erasmus": [
        "erasmus", "programa erasmus", "intercambio", "movilidad internacional",
        "estudiar en el extranjero", "becas erasmus", "plazo erasmus", "créditos erasmus"
    ],
    "Becas": [
        "becas", "solicitud beca", "beca mec", "ayuda económica", "becas universitarias",
        "requisitos beca", "plazo beca", "subvenciones", "beca general", "becas us"
    ],
    "Biblioteca": [
        "biblioteca", "catálogo de libros", "renovación préstamo", "reserva libros",
        "sala de estudio", "consulta bibliográfica", "horarios biblioteca", "préstamo libros"
    ],
    "Matrícula": [
        "matrícula", "inscripción", "plazos de matrícula", "precio matrícula",
        "documentación matrícula", "cambio de expediente", "traslado expediente",
        "reingreso", "proceso de inscripción", "cambio de carrera"
    ],
    "Calendario Académico": [
        "calendario académico", "inicio de curso", "fin de clases", "vacaciones",
        "convocatorias exámenes", "festivos", "entrega de notas", "fechas importantes"
    ],
    "Carné Universitario": [
        "carné universitario", "tarjeta universitaria", "identificación universitaria",
        "registro carné", "obtención carné", "ventajas carné universitario"
    ],
    "Deportes": [
        "deportes", "actividades deportivas", "instalaciones deportivas", "pabellón deportivo",
        "gimnasio", "competencias deportivas", "entrenamientos", "horarios deportes"
    ],
    "Comedores Universitarios": [
        "comedores universitarios", "menú comedor", "horarios comedor", "subsidio comedor",
        "tarjetas comedor", "precios comedor"
    ],
    "Correo Institucional": [
        "correo institucional", "email universitario", "acceso correo", "configuración correo",
        "soporte correo institucional"
    ],
    "Residencias y Alojamiento": [
        "residencias universitarias", "alojamiento universitario", "reserva residencia",
        "precios alojamiento", "opciones de alojamiento", "residencias estudiantes"
    ],
    "Empleo": [
        "empleo", "bolsa de trabajo", "ofertas de empleo", "prácticas profesionales", "empleo en universidad"
    ],
    "Investigación": [
        "investigación", "proyectos de investigación", "publicaciones científicas", "becas de investigación",
        "equipos de investigación", "resultados de investigación"
    ],
    "Actividades Culturales": [
        "actividades culturales", "eventos culturales", "teatro universitario", "conciertos", "cine universitario"
    ],
    "Idiomas": [
        "idiomas", "aprendizaje de idiomas", "cursos de idiomas", "exámenes de idiomas", "certificación de idiomas"
    ],
    "Intercambio Académico": [
        "intercambio académico", "programas de intercambio", "movilidad académica", "destinos intercambio"
    ],
    "Certificados": [
        "certificados", "certificación académica", "duplicados de certificados", "solicitud de certificado",
        "coste certificado", "trámite de certificado"
    ],
    "Doctorado": [
        "doctorado", "programa de doctorado", "tesis doctoral", "becas doctorado", "requisitos doctorado"
    ],
    "Secretaría": [
        "secretaría", "gestión administrativa", "trámites administrativos", "cita en secretaría", "secretaría académica"
    ],
    "Transporte Universitario": [
        "transporte universitario", "autobuses universitarios", "ruta transporte", "tarjeta de transporte", "transporte público"
    ],
    "Asociaciones Estudiantiles": [
        "asociaciones estudiantiles", "agrupaciones estudiantiles", "clubes de estudiantes", "actividades asociaciones"
    ],
    "Voluntariado": [
        "voluntariado", "programas de voluntariado", "acciones voluntarias", "organización voluntariado"
    ],
    "Investigación Científica": [
        "investigación científica", "proyectos científicos", "artículos científicos", "revistas científicas", "becas investigación científica"
    ],
    "Másteres": [
        "másteres", "programas de máster", "máster oficial", "admisión máster", "becas máster"
    ],
    "Ciberseguridad": [
        "ciberseguridad", "seguridad informática", "protección de datos", "cursos ciberseguridad", "ciberataques"
    ],
    "Títulos": [
        "título universitario", "expedición título", "diploma", "certificado académico",
        "duplicado título", "solicitud título", "coste título", "recoger título", "trámite título"
    ],
    "Equivalencia de Estudios": [
        "equivalencia de estudios", "homologación de títulos", "reconocimiento de estudios", "validación de estudios"
    ],
    "Títulos Oficiales": [
        "títulos oficiales", "grados oficiales", "másteres oficiales", "títulos universitarios oficiales"
    ],
    "Atención Psicológica": [
        "salud mental", "ayuda psicológica", "atención psicológica", "psicólogo",
        "ansiedad", "depresión", "estrés", "bienestar emocional", "orientación personal",
        "hablar con alguien"
    ],
    "Prácticas": [
        "prácticas", "prácticas profesionales", "empresa para prácticas", "requisitos prácticas",
        "horarios prácticas", "becas para prácticas"
    ],
    "Asesoramiento Académico": [
        "asesoramiento académico", "tutoría académica", "orientación académica", "consultas académicas"
    ],
    "Ayudas al Estudio": [
        "ayudas al estudio", "subvenciones académicas", "becas ayudas", "ayudas económicas", "descuentos académicos"
    ],
    "Procedimientos Administrativos": [
        "procedimientos administrativos", "gestión académica", "trámites administrativos", "registro académico"
    ],
    "Eventos Académicos": [
        "eventos académicos", "conferencias", "seminarios", "exposiciones", "charlas académicas"
    ],
    "Cambio de Carrera": [
        "cambio de carrera", "traslado de expediente", "cambio de especialidad", "cambio de titulación", "cambio de grado"
    ],
    "Redes Sociales": [
        "redes sociales", "comunicación digital", "comunicación en redes", "facebook universidad", "twitter universidad"
    ],
    "Software Universitario": [
        "software universitario", "licencias software", "plataformas online", "aplicaciones universitarias"
    ],
    "Pagos y Tasas": [
        "pagos", "tasas universitarias", "pago matrícula", "pago tasas", "documentos pagos"
    ],
    "Requisitos de Admisión": [
        "requisitos de admisión", "procesos de admisión", "documentación necesaria", "admisión grados", "requisitos máster"
    ],
    "Grados": [
        "grados", "programas de grado", "requisitos grado", "plan de estudios grado"
    ],
    "Comunicación Universitaria": [
        "comunicación universitaria", "noticias universidad", "boletín informativo", "comunicados oficiales"
    ],
    "Certificación Lingüística": [
        "certificación lingüística", "exámenes de idiomas", "certificados de idioma", "acreditación de idiomas"
    ],
    "Notas": [
        "notas", "calificaciones", "resultados académicos", "publicación de notas", "consultar notas"
    ],
    "Enseñanza Virtual": [
        "enseñanza virtual", "cursos online", "clases virtuales", "plataformas educativas", "educación online"
    ],
    "Congresos": [
        "congresos", "congresos académicos", "congresos internacionales", "seminarios académicos", "eventos científicos"
    ],
    "Correo Estudiantil": [
        "correo estudiantil", "email universitario", "acceso a correo", "configuración correo"
    ],
    "Salud y Bienestar": [
        "salud y bienestar", "bienestar universitario", "actividades de salud", "servicios médicos", "psicología"
    ],
    "Cursos de Formación": [
        "cursos de formación", "formación continua", "cursos cortos", "formación extraacadémica"
    ],
    "Orientación Laboral": [
        "orientación laboral", "empleo", "asesoría profesional", "preparación laboral", "ofertas de trabajo"
    ],
    "Revalidación de Títulos": [
        "revalidación de títulos", "homologación de título", "reconocimiento académico", "equivalencia de título"
    ],
    "Escuela de Idiomas": [
        "escuela de idiomas", "cursos de idiomas", "certificados de idiomas", "cursos intensivos"
    ],
    "Plataformas Online": [
        "plataformas online", "plataformas educativas", "cursos online", "plataformas de aprendizaje"
    ]
}

# Función para actualizar las palabras clave
def reasignar_palabras_clave(categoria):
    return ", ".join(sorted(set(palabras_clave_por_categoria.get(categoria, []))))

# Reemplazar las palabras clave
df["Palabras Clave"] = df["Categoría"].apply(reasignar_palabras_clave)

# Guardar el nuevo dataset
df.to_csv("universidad_sevilla_palabras_mejoradas.csv", index=False)

print("✅ Archivo generado: universidad_sevilla_palabras_mejoradas.csv")


