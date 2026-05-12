"""
TudiaPollito — App de práctica de exámenes tipo test
Ejecutar: streamlit run app.py
"""

import streamlit as st
import json
import re
import random
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# ─── Configuración ───
RESULTADOS_DIR = Path("resultados")
DATA_DIR = Path("data")
RESULTADOS_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="TudiaPollito", page_icon="🐥", layout="centered")

st.markdown("""
<style>
    /* ─── Paleta azul/violeta ─── */
    :root {
        --primary: #6C5CE7;
        --primary-light: #A29BFE;
        --primary-dark: #4834D4;
        --accent: #74B9FF;
        --bg-dark: #1A1A2E;
        --bg-card: #16213E;
        --bg-surface: #0F3460;
        --text-light: #E8E8F0;
        --text-muted: #A0A0C0;
        --success: #00D2A0;
        --error: #FF6B6B;
        --warning: #FECA57;
    }

    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
        color: var(--text-light);
    }
    .block-container {
        max-width: 100% !important;
        overflow-x: hidden;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }

    /* Force light text everywhere */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {
        color: #E8E8F0;
    }

    /* Headers */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #A29BFE !important;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background: rgba(108, 92, 231, 0.15);
        border: 1px solid rgba(108, 92, 231, 0.3);
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="stMetricValue"] {
        color: #A29BFE !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
    }

    /* Botones */
    .stButton > button {
        background: rgba(108, 92, 231, 0.2) !important;
        border: 1px solid rgba(108, 92, 231, 0.4) !important;
        color: var(--text-light) !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: rgba(108, 92, 231, 0.4) !important;
        border-color: var(--primary) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C5CE7, #4834D4) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7C6CF7, #5844E4) !important;
    }

    /* Checkboxes */
    .stCheckbox label {
        background: rgba(108, 92, 231, 0.1);
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 4px;
        transition: all 0.2s ease;
        word-wrap: break-word;
        overflow-wrap: break-word;
        color: #E8E8F0 !important;
    }
    .stCheckbox label:hover {
        background: rgba(108, 92, 231, 0.2);
        border-color: rgba(108, 92, 231, 0.4);
    }
    .stCheckbox label p, .stCheckbox label span {
        color: #E8E8F0 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* Mobile */
    @media (max-width: 768px) {
        .stCheckbox label {
            padding: 8px 10px;
            font-size: 0.9rem;
        }
        .stButton > button {
            font-size: 0.85rem !important;
            padding: 6px 10px !important;
        }
    }

    /* Success / Error / Warning / Info boxes */
    .stSuccess {
        background-color: rgba(0, 210, 160, 0.15) !important;
        border-left: 4px solid var(--success) !important;
        color: var(--text-light) !important;
    }
    .stError {
        background-color: rgba(255, 107, 107, 0.15) !important;
        border-left: 4px solid var(--error) !important;
        color: var(--text-light) !important;
    }
    .stWarning {
        background-color: rgba(254, 202, 87, 0.15) !important;
        border-left: 4px solid var(--warning) !important;
        color: var(--text-light) !important;
    }
    .stInfo {
        background-color: rgba(116, 185, 255, 0.12) !important;
        border-left: 4px solid var(--accent) !important;
        color: var(--text-light) !important;
    }
    [data-testid="stAlert"] {
        border-radius: 8px;
    }
    [data-testid="stAlert"] p, [data-testid="stAlert"] li,
    [data-testid="stAlert"] blockquote {
        color: var(--text-light) !important;
    }
    [data-testid="stAlert"] blockquote {
        border-left: 3px solid var(--primary-light) !important;
        padding: 10px 14px;
        margin: 8px 0;
        background: rgba(108, 92, 231, 0.08);
        border-radius: 0 6px 6px 0;
    }
    [data-testid="stAlert"] strong {
        color: #A29BFE !important;
    }
    [data-testid="stAlert"] hr {
        border-color: rgba(162, 155, 254, 0.2) !important;
        margin: 12px 0;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(108, 92, 231, 0.1) !important;
        border-radius: 8px !important;
        color: var(--text-light) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(108, 92, 231, 0.15);
        border-radius: 8px 8px 0 0;
        color: var(--text-muted);
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(108, 92, 231, 0.3) !important;
        color: var(--text-light) !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6C5CE7, #74B9FF) !important;
        border-radius: 10px;
    }

    /* Radio buttons */
    .stRadio > div {
        gap: 4px;
    }
    .stRadio label {
        background: rgba(108, 92, 231, 0.08);
        border: 1px solid rgba(108, 92, 231, 0.15);
        border-radius: 8px;
        padding: 8px 12px;
    }

    /* Divider */
    hr {
        border-color: rgba(108, 92, 231, 0.2) !important;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--primary) !important;
    }

    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(108, 92, 231, 0.3) !important;
    }

    /* Caption text */
    .stCaption, caption, .stMarkdown small {
        color: var(--text-muted) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─── Funciones de lectura de archivos ───

def listar_archivos(carpeta: str) -> list[dict]:
    ruta = DATA_DIR / carpeta
    if not ruta.exists():
        return []
    archivos = []
    for archivo in sorted(ruta.iterdir()):
        if archivo.suffix in (".md", ".txt"):
            nombre = archivo.stem.replace("_", " ").title()
            archivos.append({"nombre": nombre, "ruta": archivo})
    return archivos


def parsear_preguntas(texto: str, origen: str = "") -> list[dict]:
    preguntas = []
    bloques = re.split(r"##\s*[Pp]regunta\s*\d*", texto)

    for bloque in bloques:
        bloque = bloque.strip()
        if not bloque:
            continue

        lineas = bloque.split("\n")
        texto_pregunta = []
        opciones = []
        respuesta = None
        explicacion = ""
        leyendo_explicacion = False

        for linea in lineas:
            linea_strip = linea.strip()

            match_resp = re.match(r"[Rr]espuesta:\s*([a-eA-E,\s]+)", linea_strip)
            if match_resp:
                letras_raw = match_resp.group(1).lower().replace(" ", "")
                respuesta = [l.strip() for l in letras_raw.split(",") if l.strip()]
                leyendo_explicacion = False
                continue

            match_expl = re.match(r"[Ee]xplicaci[oó]n:\s*(.*)", linea_strip)
            if match_expl:
                explicacion = match_expl.group(1)
                leyendo_explicacion = True
                continue

            if leyendo_explicacion and linea_strip:
                explicacion += " " + linea_strip
                continue

            match_opt = re.match(r"[-*]?\s*([a-eA-E])\)\s*(.*)", linea_strip)
            if match_opt:
                opciones.append({
                    "letra": match_opt.group(1).lower(),
                    "texto": match_opt.group(2).strip()
                })
                leyendo_explicacion = False
                continue

            if linea_strip and not opciones:
                texto_pregunta.append(linea_strip)

        if texto_pregunta and opciones and respuesta:
            preguntas.append({
                "texto": " ".join(texto_pregunta),
                "opciones": opciones,
                "respuesta": respuesta,
                "explicacion": explicacion.strip() if explicacion.strip() else None,
                "origen": origen,
                "multiple": len(respuesta) > 1,
            })

    return preguntas


def cargar_temario() -> str:
    archivos = listar_archivos("temario")
    textos = []
    for a in archivos:
        textos.append(a["ruta"].read_text(encoding="utf-8"))
    return "\n\n".join(textos)


def cargar_preguntas(filtro_archivos: list[str] | None = None) -> list[dict]:
    preguntas = []
    for carpeta in ("examenes_resueltos", "examenes_sin_resolver"):
        archivos = listar_archivos(carpeta)
        for a in archivos:
            if filtro_archivos is not None and a["nombre"] not in filtro_archivos:
                continue
            texto = a["ruta"].read_text(encoding="utf-8")
            preguntas.extend(parsear_preguntas(texto, origen=a["nombre"]))
    return preguntas


def listar_temas_disponibles() -> list[str]:
    temas = set()
    for carpeta in ("examenes_resueltos", "examenes_sin_resolver"):
        for a in listar_archivos(carpeta):
            temas.add(a["nombre"])
    return sorted(temas)


def barajar_opciones(pregunta: dict) -> dict:
    p = pregunta.copy()
    opciones = list(p["opciones"])
    respuestas_correctas = set(p["respuesta"])

    textos_correctos = {opt["texto"] for opt in opciones if opt["letra"] in respuestas_correctas}

    random.shuffle(opciones)
    letras = ["a", "b", "c", "d", "e"]
    nuevas_opciones = []
    nuevas_respuestas = []

    for i, opt in enumerate(opciones):
        nueva_letra = letras[i] if i < len(letras) else opt["letra"]
        if opt["texto"] in textos_correctos:
            nuevas_respuestas.append(nueva_letra)
        nuevas_opciones.append({"letra": nueva_letra, "texto": opt["texto"]})

    p["opciones"] = nuevas_opciones
    p["respuesta"] = sorted(nuevas_respuestas)
    p["multiple"] = len(nuevas_respuestas) > 1
    return p


# ─── Funciones de resultados ───

def id_pregunta(pregunta: dict) -> str:
    return hashlib.md5(pregunta["texto"].encode()).hexdigest()[:12]


def guardar_resultado(resultado: dict):
    archivo = RESULTADOS_DIR / "historial.json"
    historial = []
    if archivo.exists():
        historial = json.loads(archivo.read_text(encoding="utf-8"))
    historial.append(resultado)
    archivo.write_text(json.dumps(historial, ensure_ascii=False, indent=2), encoding="utf-8")


def cargar_historial() -> list[dict]:
    archivo = RESULTADOS_DIR / "historial.json"
    if archivo.exists():
        return json.loads(archivo.read_text(encoding="utf-8"))
    return []


def obtener_preguntas_falladas() -> set[str]:
    historial = cargar_historial()
    falladas = set()
    for h in historial:
        for f in h.get("falladas", []):
            falladas.add(f)
    return falladas


# ─── Generar explicación desde temario ───

def _es_encabezado(linea: str) -> bool:
    if re.match(r"^#+\s", linea):
        return True
    if re.match(r"^TEMA\s+\d+", linea):
        return True
    if re.match(r"^-+PARCIAL", linea):
        return True
    letras = re.sub(r"[^a-záéíóúñü]", "", linea.lower())
    if len(letras) >= 4 and linea == linea.upper() and len(linea) < 120:
        return True
    return False


def _limpiar_texto_pdf(texto: str) -> str:
    texto = re.sub(r"[«»\^|{}~±]", " ", texto)
    texto = re.sub(r"\(\s*\)", "", texto)
    texto = re.sub(r"FIGURA\s+\d+[-–]\d+[^.]{0,200}\.", "", texto)
    texto = re.sub(r"TABLA\s+\d+[-–]\d+[^.]{0,200}\.", "", texto)
    texto = re.sub(r"F[KI]G?URA\s+\d+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"(?:\b[A-Z]{1,3}[0-9]*\s*[''\"*→←↔\-]+\s*){2,}", " ", texto)
    texto = re.sub(r"(?:[A-Z]{1,2}['\"]?\s+){4,}", " ", texto)
    texto = re.sub(r"\s{2,}", " ", texto)
    return texto.strip()


def _cortar_en_frase(texto: str, objetivo: int) -> int:
    if len(texto) <= objetivo:
        return len(texto)
    corte = texto.rfind(". ", 0, objetivo + 50)
    if corte > objetivo * 0.6:
        return corte + 1
    return objetivo


def _segmentar_temario(temario: str) -> list[str]:
    lineas = temario.split("\n")
    limpias = []
    for linea in lineas:
        stripped = linea.strip()
        if not stripped:
            continue
        if re.match(r"^(Apuntes BQ|p[aá]g\.\s*\d+|---)", stripped, re.IGNORECASE):
            continue
        if re.match(r"^\d+$", stripped):
            continue
        if stripped == "•":
            continue
        limpias.append(stripped)

    secciones = []
    actual = []
    for linea in limpias:
        if _es_encabezado(linea) and actual:
            secciones.append(" ".join(actual))
            actual = [linea]
        else:
            actual.append(linea)
    if actual:
        secciones.append(" ".join(actual))

    ventanas = []
    tam_ventana = 900
    solapamiento = 150
    for sec in secciones:
        sec = _limpiar_texto_pdf(sec)
        if len(sec) <= tam_ventana + 100:
            if len(sec) > 40:
                ventanas.append(sec)
        else:
            pos = 0
            while pos < len(sec):
                fin = _cortar_en_frase(sec[pos:], tam_ventana)
                trozo = sec[pos:pos + fin].strip()
                if len(trozo) > 40:
                    ventanas.append(trozo)
                avance = max(fin - solapamiento, 200)
                pos += avance
                if pos + 100 >= len(sec):
                    break

    return ventanas


PALABRAS_COMUNES = {
    "el", "la", "los", "las", "un", "una", "de", "del", "en", "y", "o",
    "que", "es", "son", "por", "para", "con", "se", "su", "al", "lo",
    "como", "más", "no", "si", "cuál", "qué", "cual", "entre", "sobre",
    "esta", "este", "estas", "estos", "ha", "han", "ser", "fue", "sido",
    "tiene", "puede", "cuando", "donde", "sino", "también", "todo", "todos",
    "cada", "muy", "ya", "hay", "cual", "cuales", "siguiente", "siguientes",
    "según", "respecto", "través", "partir", "dentro", "forma", "manera",
    "partir", "tipo", "tipos", "proceso", "parte", "produce", "lugar",
    "mediante", "través", "nivel", "función", "reacción", "molécula",
}


def _extraer_keywords(texto: str) -> set[str]:
    return set(re.findall(r"\b[a-záéíóúñü]{4,}\b", texto.lower())) - PALABRAS_COMUNES


def _extraer_bigramas(texto: str) -> set[str]:
    palabras = re.findall(r"\b[a-záéíóúñü]{3,}\b", texto.lower())
    return {f"{palabras[i]} {palabras[i+1]}" for i in range(len(palabras) - 1)}


def buscar_explicacion_temario(pregunta: dict, temario: str) -> str:
    if pregunta.get("explicacion"):
        return pregunta["explicacion"]

    respuestas_correctas = pregunta["respuesta"]

    textos_correctas = []
    for opt in pregunta["opciones"]:
        if opt["letra"] in respuestas_correctas:
            textos_correctas.append(f"**{opt['letra']}) {opt['texto']}**")

    header = "Las respuestas correctas son:\n\n" + "\n\n".join(f"- {t}" for t in textos_correctas)

    if not temario:
        return header

    texto_respuestas = " ".join(
        opt["texto"] for opt in pregunta["opciones"] if opt["letra"] in respuestas_correctas
    )
    texto_enunciado = pregunta["texto"]

    kw_pregunta = _extraer_keywords(texto_enunciado)
    kw_respuesta = _extraer_keywords(texto_respuestas)
    kw_solo_respuesta = kw_respuesta - kw_pregunta

    bigramas_pregunta = _extraer_bigramas(texto_enunciado)
    bigramas_respuesta = _extraer_bigramas(texto_respuestas)

    ventanas = _segmentar_temario(temario)
    puntuados = []
    for ventana in ventanas:
        ventana_lower = ventana.lower()
        score = sum(1 for p in kw_pregunta if p in ventana_lower)
        score += sum(3 for p in kw_solo_respuesta if p in ventana_lower)
        score += sum(2 for p in kw_respuesta if p in ventana_lower)
        score += sum(2 for b in bigramas_pregunta if b in ventana_lower)
        score += sum(4 for b in bigramas_respuesta if b in ventana_lower)
        if score >= 5:
            puntuados.append((score, ventana))

    puntuados.sort(key=lambda x: x[0], reverse=True)

    if puntuados:
        fragmentos = []
        textos_vistos = set()
        for _, p in puntuados[:8]:
            palabras_reales = re.findall(r"\b[a-záéíóúñü]{4,}\b", p.lower())
            ratio_texto = len(" ".join(palabras_reales)) / max(len(p), 1)
            if len(palabras_reales) < 25 or ratio_texto < 0.35:
                continue
            corte = _cortar_en_frase(p, 1000)
            p = p[:corte]
            p_corto = p[:120]
            if p_corto not in textos_vistos:
                textos_vistos.add(p_corto)
                fragmentos.append(p)
            if len(fragmentos) >= 2:
                break

        if fragmentos:
            return (
                header + "\n\n"
                "📖 **Del temario:**\n\n"
                + "\n\n---\n\n".join(f"> {f}" for f in fragmentos)
            )

    return header


# ─── Inicializar estado ───

def init_estado():
    defaults = {
        "pagina": "inicio",
        "preguntas": [],
        "indice": 0,
        "respuestas": {},
        "mostrar_resultado": False,
        "modo": "practica",
        "examen_terminado": False,
        "num_preguntas": 10,
        "temporizador_activo": False,
        "tiempo_limite_min": 15,
        "tiempo_inicio": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_estado()


# ─── Estadísticas ───

def mostrar_estadisticas(historial: list[dict]):
    if len(historial) < 2:
        st.info("Necesitas al menos 2 intentos para ver estadísticas.")
        return

    porcentajes = [h["porcentaje"] for h in historial]

    st.markdown("**Evolución de puntuación**")
    st.line_chart(porcentajes, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    media = sum(porcentajes) / len(porcentajes)
    with col1:
        st.metric("Media", f"{media:.0f}%")
    with col2:
        st.metric("Mejor nota", f"{max(porcentajes)}%")
    with col3:
        st.metric("Total intentos", len(historial))

    modos = {}
    for h in historial:
        m = h.get("modo", "desconocido")
        modos.setdefault(m, []).append(h["porcentaje"])

    if len(modos) > 1:
        st.markdown("**Por modo**")
        for m, ps in modos.items():
            avg = sum(ps) / len(ps)
            st.markdown(f"- **{m.capitalize()}**: {len(ps)} intentos, media {avg:.0f}%")


# ─── Páginas ───

def pagina_inicio():
    st.title("🐥 TudiaPollito")
    st.markdown("**Practica tus exámenes tipo test — Bioquímica**")
    st.divider()

    preguntas_todas = cargar_preguntas()
    temario = cargar_temario()
    temas = listar_temas_disponibles()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Preguntas disponibles", len(preguntas_todas))
    with col2:
        st.metric("Temario cargado", "Sí" if temario else "No")

    if not preguntas_todas:
        st.warning(
            "No hay preguntas cargadas. Añade archivos `.md` o `.txt` en:\n\n"
            "- `data/examenes_resueltos/`\n"
            "- `data/examenes_sin_resolver/`\n\n"
            "Consulta el README.md para ver el formato."
        )
        return

    st.divider()

    preguntas_filtradas = preguntas_todas

    # Selección de modo
    opciones_modo = [
        "🎯 Práctica",
        "📋 Examen",
        "🔁 Repaso",
    ]
    modo = st.pills(
        "Modo",
        opciones_modo,
        default="🎯 Práctica",
        label_visibility="collapsed",
    )
    if modo is None:
        modo = "🎯 Práctica"

    es_repaso = "Repaso" in modo

    if es_repaso:
        ids_falladas = obtener_preguntas_falladas()
        preguntas_filtradas = [p for p in preguntas_filtradas if id_pregunta(p) in ids_falladas]
        if not preguntas_filtradas:
            st.info("🎉 No tienes preguntas falladas pendientes de repaso.")
            return
        st.info(f"Hay **{len(preguntas_filtradas)}** preguntas falladas disponibles para repasar.")

    max_preguntas = min(len(preguntas_filtradas), 50)
    if max_preguntas < 5:
        num = st.slider(
            "Número de preguntas:",
            min_value=1,
            max_value=max(max_preguntas, 1),
            value=max(max_preguntas, 1),
            step=1,
        )
    else:
        num = st.slider(
            "Número de preguntas:",
            min_value=5,
            max_value=max_preguntas,
            value=min(10, max_preguntas),
            step=5,
        )

    # Opciones adicionales
    opciones_extra = ["🔀 Barajar opciones"]
    if "Examen" in modo:
        opciones_extra.append("⏱️ Temporizador")
    seleccion_extra = st.pills(
        "Opciones",
        opciones_extra,
        selection_mode="multi",
        default=[],
        label_visibility="collapsed",
    )
    barajar = "🔀 Barajar opciones" in seleccion_extra
    usar_temporizador = "⏱️ Temporizador" in seleccion_extra

    tiempo_min = 15
    if usar_temporizador:
        tiempo_min = st.slider(
            "Minutos para completar:", min_value=5, max_value=60, value=15, step=5
        )

    if st.button("▶️ Empezar", type="primary", use_container_width=True):
        seleccion = random.sample(preguntas_filtradas, min(num, len(preguntas_filtradas)))
        if barajar:
            seleccion = [barajar_opciones(p) for p in seleccion]
        st.session_state.preguntas = seleccion
        st.session_state.indice = 0
        st.session_state.respuestas = {}
        st.session_state.mostrar_resultado = False
        st.session_state.examen_terminado = False
        st.session_state.modo = "repaso" if es_repaso else ("practica" if "Práctica" in modo else "examen")
        st.session_state.num_preguntas = num
        st.session_state.temporizador_activo = usar_temporizador
        st.session_state.tiempo_limite_min = tiempo_min
        st.session_state.tiempo_inicio = datetime.now().isoformat() if usar_temporizador else None
        st.session_state.pagina = "examen"
        st.rerun()

    # Historial y estadísticas
    historial = cargar_historial()
    if historial:
        st.divider()
        tab_hist, tab_stats = st.tabs(["📊 Últimos resultados", "📈 Estadísticas"])

        with tab_hist:
            for h in reversed(historial[-5:]):
                color = "🟢" if h["porcentaje"] >= 70 else "🟡" if h["porcentaje"] >= 50 else "🔴"
                st.markdown(
                    f"{color} **{h['fecha']}** — {h['aciertos']}/{h['total']} "
                    f"({h['porcentaje']}%) — Modo: {h['modo']}"
                )

        with tab_stats:
            mostrar_estadisticas(historial)


def finalizar_examen():
    preguntas = st.session_state.preguntas
    total = len(preguntas)
    modo = st.session_state.modo

    st.session_state.examen_terminado = True
    aciertos = sum(1 for r in st.session_state.respuestas.values() if r["correcta"])
    falladas = [
        id_pregunta(preguntas[i])
        for i in range(total)
        if i in st.session_state.respuestas and not st.session_state.respuestas[i]["correcta"]
    ]
    guardar_resultado({
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "modo": modo,
        "aciertos": aciertos,
        "total": total,
        "porcentaje": round(aciertos / total * 100),
        "falladas": falladas,
    })
    st.session_state.pagina = "resultados"
    st.rerun()


def comprobar_respuesta(pregunta, letras_seleccionadas):
    correctas = set(pregunta["respuesta"])
    seleccionadas = set(letras_seleccionadas)
    return correctas == seleccionadas


PREGUNTAS_POR_PAGINA = 3


def pagina_examen():
    preguntas = st.session_state.preguntas
    total = len(preguntas)
    modo = st.session_state.modo
    pag = st.session_state.indice
    total_paginas = (total + PREGUNTAS_POR_PAGINA - 1) // PREGUNTAS_POR_PAGINA

    if not preguntas:
        st.session_state.pagina = "inicio"
        st.rerun()
        return

    # Temporizador
    tiempo_restante = None
    if st.session_state.temporizador_activo and st.session_state.tiempo_inicio:
        inicio = datetime.fromisoformat(st.session_state.tiempo_inicio)
        limite = inicio + timedelta(minutes=st.session_state.tiempo_limite_min)
        ahora = datetime.now()
        tiempo_restante = (limite - ahora).total_seconds()

        if tiempo_restante <= 0:
            st.session_state.examen_terminado = True
            aciertos = sum(1 for r in st.session_state.respuestas.values() if r["correcta"])
            falladas = [
                id_pregunta(preguntas[i])
                for i in range(total)
                if i not in st.session_state.respuestas
                or not st.session_state.respuestas[i]["correcta"]
            ]
            guardar_resultado({
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "modo": modo,
                "aciertos": aciertos,
                "total": total,
                "porcentaje": round(aciertos / total * 100),
                "falladas": falladas,
            })
            st.session_state.pagina = "resultados"
            st.rerun()
            return

    inicio_pag = pag * PREGUNTAS_POR_PAGINA
    fin_pag = min(inicio_pag + PREGUNTAS_POR_PAGINA, total)

    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("✕ Salir"):
            st.session_state.pagina = "inicio"
            st.rerun()
    with col2:
        st.progress(fin_pag / total, text=f"Preguntas {inicio_pag + 1}–{fin_pag} de {total}")
    with col3:
        if tiempo_restante is not None:
            mins = int(tiempo_restante // 60)
            secs = int(tiempo_restante % 60)
            icono = "🔴" if mins < 2 else "🟡" if mins < 5 else "⏱️"
            st.markdown(f"{icono} **{mins}:{secs:02d}**")
        else:
            respondidas = len(st.session_state.respuestas)
            st.markdown(f"**{respondidas}/{total}**")

    st.divider()

    # Renderizar las preguntas de esta página
    for idx in range(inicio_pag, fin_pag):
        pregunta = preguntas[idx]

        if pregunta.get("origen"):
            st.caption(f"📁 {pregunta['origen']}")

        multi = len(pregunta.get("respuesta", [])) > 1
        titulo_q = f"### Pregunta {idx + 1}: {pregunta['texto']}"
        if multi:
            titulo_q += "\n*(varias respuestas son correctas)*"
        st.markdown(titulo_q)

        ya_respondida = idx in st.session_state.respuestas

        _render_pregunta_checkboxes(pregunta, idx, ya_respondida, modo)

        if modo in ("practica", "repaso") and ya_respondida:
            _mostrar_feedback(pregunta, idx)

        if modo == "examen" and st.session_state.examen_terminado and ya_respondida:
            _mostrar_feedback(pregunta, idx)

        st.divider()

    # Navegación
    col_prev, col_mid, col_next = st.columns([1, 2, 1])

    with col_prev:
        if pag > 0:
            if st.button("← Anterior", use_container_width=True):
                st.session_state.indice = pag - 1
                st.rerun()

    with col_next:
        if pag < total_paginas - 1:
            if st.button("Siguiente →", use_container_width=True):
                st.session_state.indice = pag + 1
                st.rerun()
        elif len(st.session_state.respuestas) == total:
            if modo == "examen" and not st.session_state.examen_terminado:
                if st.button("📋 Ver resultados", type="primary", use_container_width=True):
                    finalizar_examen()
            elif modo in ("practica", "repaso"):
                if st.button("📊 Ver resumen", type="primary", use_container_width=True):
                    finalizar_examen()

    # Navegación rápida por páginas
    with col_mid:
        max_nav = min(total_paginas, 10)
        cols = st.columns(max_nav)
        for i in range(max_nav):
            with cols[i]:
                pg_inicio = i * PREGUNTAS_POR_PAGINA
                pg_fin = min(pg_inicio + PREGUNTAS_POR_PAGINA, total)
                todas_respondidas = all(j in st.session_state.respuestas for j in range(pg_inicio, pg_fin))
                label = "●" if todas_respondidas else "○"
                if st.button(label, key=f"nav_{i}", help=f"Preguntas {pg_inicio+1}–{pg_fin}"):
                    st.session_state.indice = i
                    st.rerun()


def _render_pregunta_checkboxes(pregunta, indice, ya_respondida, modo):
    seleccion_previa = st.session_state.respuestas.get(indice, {}).get("letras", [])

    if not ya_respondida or (modo == "examen" and not st.session_state.examen_terminado):
        seleccionadas = []
        for opt in pregunta["opciones"]:
            checked = opt["letra"] in seleccion_previa
            val = st.checkbox(
                f"{opt['letra']}) {opt['texto']}",
                value=checked,
                key=f"cb_{indice}_{opt['letra']}",
            )
            if val:
                seleccionadas.append(opt["letra"])

        if st.button("✔ Confirmar respuesta", key=f"confirm_{indice}", use_container_width=True, type="primary"):
            if seleccionadas:
                es_correcta = comprobar_respuesta(pregunta, seleccionadas)
                st.session_state.respuestas[indice] = {
                    "letras": seleccionadas,
                    "correcta": es_correcta,
                }
                st.rerun()
            else:
                st.warning("Selecciona al menos una opción.")
    else:
        correctas = set(pregunta["respuesta"])
        elegidas = set(seleccion_previa)
        for opt in pregunta["opciones"]:
            letra = opt["letra"]
            es_correcta = letra in correctas
            fue_elegida = letra in elegidas
            if es_correcta and fue_elegida:
                color, icono = "#A29BFE", "✅"
            elif es_correcta and not fue_elegida:
                color, icono = "#A29BFE", "✅"
            elif not es_correcta and fue_elegida:
                color, icono = "#FF6B6B", "❌"
            else:
                color, icono = "#A0A0C0", ""
            st.markdown(
                f'<p style="color:{color}; margin:4px 0;">'
                f'{icono} {letra}) {opt["texto"]}</p>',
                unsafe_allow_html=True,
            )


def _mostrar_feedback(pregunta, indice):
    resp = st.session_state.respuestas[indice]
    if resp["correcta"]:
        st.success("✅ ¡Correcto!")
    else:
        st.error("❌ Incorrecto")
        temario = cargar_temario()
        explicacion = buscar_explicacion_temario(pregunta, temario)
        st.info(explicacion)


def pagina_resultados():
    preguntas = st.session_state.preguntas
    respuestas = st.session_state.respuestas
    total = len(preguntas)
    aciertos = sum(1 for r in respuestas.values() if r["correcta"])
    porcentaje = round(aciertos / total * 100) if total > 0 else 0

    st.title("📊 Resultados")
    st.divider()

    if porcentaje >= 70:
        st.success(f"## ✅ {porcentaje}% — {aciertos}/{total} correctas")
        st.balloons()
    elif porcentaje >= 50:
        st.warning(f"## ⚠️ {porcentaje}% — {aciertos}/{total} correctas")
    else:
        st.error(f"## ❌ {porcentaje}% — {aciertos}/{total} correctas")

    st.divider()

    temario = cargar_temario()
    for i, pregunta in enumerate(preguntas):
        resp = respuestas.get(i, {})
        icono = "✅" if resp.get("correcta") else "❌"
        titulo = pregunta["texto"][:80]
        letras_usuario = resp.get("letras", [])

        with st.expander(f"{icono} Pregunta {i+1}: {titulo}..."):
            st.markdown(f"**{pregunta['texto']}**")

            for opt in pregunta["opciones"]:
                marca = ""
                if opt["letra"] in pregunta["respuesta"] and opt["letra"] in letras_usuario:
                    marca = " ✅"
                elif opt["letra"] in pregunta["respuesta"]:
                    marca = " 🟢 (correcta)"
                elif opt["letra"] in letras_usuario:
                    marca = " ❌"
                st.markdown(f"- {opt['letra']}) {opt['texto']}{marca}")

            if not resp.get("correcta"):
                explicacion = buscar_explicacion_temario(pregunta, temario)
                st.info(explicacion)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Volver al inicio", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.rerun()
    with col2:
        if st.button("🔄 Nuevo examen", type="primary", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.rerun()


# ─── Router ───

paginas = {
    "inicio": pagina_inicio,
    "examen": pagina_examen,
    "resultados": pagina_resultados,
}

paginas[st.session_state.pagina]()
