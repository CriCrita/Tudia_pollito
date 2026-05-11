# ExamForge

App local para practicar exámenes tipo test. Sin internet, sin cuentas, sin complicaciones.

## Instalar

```bash
pip install streamlit
```

## Ejecutar

```bash
cd examforge
streamlit run app.py
```

Se abre automáticamente en el navegador (http://localhost:8501).

## Añadir tus preguntas y temario

Mete archivos `.md` o `.txt` en estas carpetas:

```
data/
├── temario/                  ← tus apuntes/temario
├── examenes_resueltos/       ← exámenes con respuesta y explicación
└── examenes_sin_resolver/    ← exámenes solo con respuesta correcta
```

### Formato de las preguntas

Cada pregunta sigue este formato (copia y pega):

```markdown
## Pregunta 1
¿Texto de la pregunta?
- a) Primera opción
- b) Segunda opción
- c) Tercera opción
- d) Cuarta opción
Respuesta: b
Explicación: Texto que explica por qué b es correcta. (Opcional)
```

**Reglas:**
- Cada pregunta empieza con `## Pregunta` (el número da igual)
- Las opciones van con `- a)`, `- b)`, `- c)`, `- d)`
- La respuesta es una letra: `Respuesta: b`
- La explicación es opcional. Si no la pones, la app busca automáticamente en el temario

### Formato del temario

Texto libre en `.md` o `.txt`. Escribe los apuntes como quieras. La app busca en el temario las partes relevantes cuando fallas una pregunta.

## Cómo funciona

1. **Inicio** — Ves cuántas preguntas hay y eliges modo:
   - **Práctica**: ves si aciertas después de cada pregunta + explicación si fallas
   - **Examen**: respondes todo y ves resultados al final
2. **Preguntas** — Una pregunta por pantalla, eliges respuesta pulsando
3. **Resultados** — Nota final, detalle de cada pregunta, explicaciones de los fallos

Los resultados se guardan automáticamente en `resultados/historial.json`.

## Estructura del proyecto

```
examforge/
├── app.py                  ← la app (único archivo de código)
├── requirements.txt        ← dependencias (solo streamlit)
├── README.md               ← este archivo
├── PROJECT_CONTEXT.md      ← contexto para Claude Code
├── data/
│   ├── temario/            ← archivos .md/.txt con el temario
│   ├── examenes_resueltos/ ← preguntas con explicación
│   └── examenes_sin_resolver/ ← preguntas sin explicación
└── resultados/
    └── historial.json      ← se crea automáticamente
```
