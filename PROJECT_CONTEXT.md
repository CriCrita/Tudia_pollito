# PROJECT_CONTEXT.md — ExamForge

## Objetivo
App local de práctica de exámenes tipo test. Lee preguntas de archivos .md, las muestra una a una, corrige, explica fallos con el temario, guarda puntuaciones.

## Stack
- Python + Streamlit
- Archivos locales (.md/.txt)
- localStorage = archivos JSON en `resultados/`
- SIN base de datos, SIN APIs, SIN backend, SIN internet

## Estructura
```
examforge/
├── app.py                    ← TODO el código (archivo único)
├── requirements.txt          ← solo streamlit
├── data/temario/             ← .md/.txt con apuntes
├── data/examenes_resueltos/  ← preguntas + respuesta + explicación
├── data/examenes_sin_resolver/ ← preguntas + respuesta (sin explicación)
└── resultados/historial.json ← se genera automáticamente
```

## Formato preguntas (.md)
```
## Pregunta 1
¿Enunciado?
- a) Opción A
- b) Opción B
- c) Opción C
- d) Opción D
Respuesta: b
Explicación: Texto opcional.
```

## Funcionalidades implementadas
- [x] Lectura de archivos .md/.txt de las 3 carpetas
- [x] Parser de preguntas con regex
- [x] Modo práctica (feedback inmediato)
- [x] Modo examen (resultados al final)
- [x] Selección de nº de preguntas
- [x] Navegación entre preguntas (anterior/siguiente/directa)
- [x] Corrección automática
- [x] Explicación de fallos (primero busca explicación del archivo, luego busca en temario por keywords)
- [x] Barra de progreso
- [x] Pantalla de resultados con detalle expandible
- [x] Historial de intentos guardado en JSON
- [x] Últimos 5 resultados en pantalla de inicio
- [x] Filtrar por tema (multiselect de archivos de examen disponibles)
- [x] Modo repaso (solo preguntas falladas anteriormente, identificadas por hash)
- [x] Estadísticas detalladas (evolución en el tiempo, media, mejor nota, desglose por modo)
- [x] Temporizador opcional en modo examen (configurable 5-60 min, auto-submit al agotar)
- [x] Barajar orden de opciones dentro de cada pregunta (checkbox opcional)
- [x] Etiqueta de origen (muestra de qué archivo viene cada pregunta)

## Siguientes pasos recomendados
1. Soporte para .docx y .pdf (añadir python-docx y PyMuPDF a requirements)
2. Exportar resultados a PDF o CSV
3. Modo oscuro / personalización visual
4. Preguntas con imágenes (soporte de imágenes embebidas en .md)

## Normas para modificaciones
1. TODO el código va en app.py — NO crear más archivos Python
2. NO añadir bases de datos
3. NO añadir APIs externas ni llamadas a internet
4. NO añadir frameworks frontend (React, Vue, etc.)
5. NO añadir Docker
6. NO añadir autenticación
7. Mantener requirements.txt con el mínimo de dependencias
8. Usar solo funciones de Python estándar + Streamlit
9. Los datos siempre en archivos locales (.md, .txt, .json)
10. Mobile-friendly (Streamlit lo gestiona solo)

## Instrucciones para Claude Code
- Lee este archivo antes de hacer cambios
- No propongas migrar a otro framework
- Si añades funcionalidad, actualiza la lista de "Funcionalidades implementadas"
- Si añades dependencias, actualiza requirements.txt Y este archivo
- Mantén app.py como archivo único — no fragmentar en módulos
- Prioriza simplicidad sobre arquitectura
