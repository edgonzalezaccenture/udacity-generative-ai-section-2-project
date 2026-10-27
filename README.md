# Proyecto: sistema de chat RAG sobre misiones de la NASA (Udacity Generative AI, sección 2)

Proyecto de la sección 2 del curso **Generative AI** de Udacity.

**Reto:** construir un sistema de preguntas y respuestas sobre las misiones Apollo 11, Apollo 13 y Challenger, basado en transcripciones y documentos técnicos reales de la NASA. Es un sistema RAG completo: un pipeline que trocea los textos, genera embeddings y los guarda en ChromaDB; un cliente RAG que recupera el contexto; un cliente LLM con la API de OpenAI; una evaluación en tiempo real con RAGAS, y una app de chat en Streamlit.

## Documentación

Documentación de la formación, en el mismo orden en que aparece en el curso:

| Archivo | Qué es |
|---|---|
| [docs/01-resumen-del-proyecto.md](docs/01-resumen-del-proyecto.md) | Resumen del proyecto: la misión, los cinco componentes que hay que construir y cómo se evalúa. |
| [docs/02-configuracion-del-entorno.md](docs/02-configuracion-del-entorno.md) | Entorno: Python, los SDK de OpenAI, Chroma y RAGAS, y la instalación en una máquina local. |
