# Proyecto: sistema de chat RAG sobre misiones de la NASA (Udacity Generative AI, sección 2)

Proyecto de la sección 2 del curso **Generative AI** de Udacity.

**Reto:** construir un sistema de preguntas y respuestas sobre las misiones Apollo 11, Apollo 13 y Challenger, basado en transcripciones y documentos técnicos reales de la NASA. Es un sistema RAG completo: un pipeline que trocea los textos, genera embeddings y los guarda en ChromaDB; un cliente RAG que recupera el contexto; un cliente LLM con la API de OpenAI; una evaluación en tiempo real con RAGAS, y una app de chat en Streamlit.

## Documentación

Documentación de la formación, en el mismo orden en que aparece en el curso:

| Archivo | Qué es |
|---|---|
| [docs/01-resumen-del-proyecto.md](docs/01-resumen-del-proyecto.md) | Resumen del proyecto: la misión, los cinco componentes que hay que construir y cómo se evalúa. |
| [docs/02-configuracion-del-entorno.md](docs/02-configuracion-del-entorno.md) | Entorno: Python, los SDK de OpenAI, Chroma y RAGAS, y la instalación en una máquina local. |
| [docs/03-instrucciones.md](docs/03-instrucciones.md) | Instrucciones: enlace al código inicial de Udacity, los cinco archivos con sus tareas (`llm_client.py`, `rag_client.py`, `embedding_pipeline.py`, `ragas_evaluator.py` y `chat.py`) y la lista de verificación de la entrega, con `evaluation_dataset.txt` y el `.zip`. |
| [docs/04-rubrica.md](docs/04-rubrica.md) | Rúbrica oficial: criterios del pipeline de embeddings (segmentación, metadatos, `--update-mode`, ChromaDB), de la recuperación e integración con el LLM y de la evaluación con RAGAS, incluido el conjunto de preguntas de prueba. |
| [docs/05-guia-del-proyecto.md](docs/05-guia-del-proyecto.md) | Guía del proyecto (en inglés): cómo ejecutar cada componente, resultados de la evaluación, dificultades encontradas y el arreglo de RAGAS 0.4.3. |

## Contenido de la entrega

| Archivo | Qué es |
|---|---|
| [embedding_pipeline.py](embedding_pipeline.py) | Pipeline de embeddings: segmentación con `--chunk-size`/`--chunk-overlap`, embeddings de OpenAI, metadatos por fragmento, `--update-mode` (`skip`/`update`/`replace`) y `--stats-only`. |
| [rag_client.py](rag_client.py) | Cliente RAG: conexión a ChromaDB, búsqueda top-k con filtro por misión y construcción del contexto con fuentes. |
| [llm_client.py](llm_client.py) | Cliente LLM: prompt del sistema de experto de la NASA, historial de conversación y llamada a OpenAI. |
| [ragas_evaluator.py](ragas_evaluator.py) | Evaluador RAGAS: relevancia de la respuesta y fidelidad, más BLEU, ROUGE y precisión del contexto cuando hay referencia. |
| [chat.py](chat.py) | App de chat en Streamlit con métricas en tiempo real. |
| [batch_evaluate.py](batch_evaluate.py) | Evaluación por lotes sobre `evaluation_dataset.txt`, con resultado por pregunta y agregado por métrica. |
| [evaluation_dataset.txt](evaluation_dataset.txt) | 9 preguntas de prueba con su respuesta esperada (resumen, emergencia, análisis de desastres, tripulación, técnico y cronología). |
| [evaluation_results.csv](evaluation_results.csv) · [evaluation_output.txt](evaluation_output.txt) | Resultados de la última evaluación por lotes. |
| [test_chat.py](test_chat.py) · [chat_test_output.txt](chat_test_output.txt) | Prueba de extremo a extremo del chat (sin navegador): 3 turnos con filtro por misión y pregunta de seguimiento, y su resultado. |
| [data_text/](data_text/) | Textos de la NASA usados por el pipeline. |
| [nasa_rag_project.zip](nasa_rag_project.zip) | Paquete de entrega para Udacity. |

## Cómo ejecutarlo

```bash
pip install -r requirements.txt          # y aplicar el arreglo de RAGAS de docs/05-guia-del-proyecto.md
echo "OPENAI_API_KEY=tu-clave" > .env

python embedding_pipeline.py --data-path ./data_text --chunk-size 1000 --chunk-overlap 200
python embedding_pipeline.py --stats-only
python batch_evaluate.py --dataset evaluation_dataset.txt --use-mission-filter --n-results 8
streamlit run chat.py
PYTHONPATH=. python test_chat.py          # prueba del chat sin navegador
```

## Resultados de la evaluación

`gpt-4o-mini`, top-k = 8, filtro por misión activado, 9 preguntas:

| Métrica | Media | Mín. | Máx. |
|---|---|---|---|
| Relevancia de la respuesta | 0.560 | 0.000 | 0.955 |
| Fidelidad | 0.797 | 0.000 | 1.000 |
| BLEU | 0.035 | 0.000 | 0.112 |
| ROUGE | 0.269 | 0.114 | 0.434 |

Las preguntas con relevancia 0 son respuestas en las que el modelo indica que el contexto recuperado no basta, en lugar de inventar. El análisis completo está en [docs/05-guia-del-proyecto.md](docs/05-guia-del-proyecto.md).
