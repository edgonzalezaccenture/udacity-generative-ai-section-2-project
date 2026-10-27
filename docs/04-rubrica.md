# Rúbrica

Utilice esta rúbrica del proyecto para comprender y evaluar los criterios del proyecto.

## Pipeline de embeddings y datos

| Criterios | Requisitos de entrega |
|---|---|
| El código demuestra una estrategia de segmentación | • Utiliza parámetros configurables `chunk_size` y `chunk_overlap` en tiempo de ejecución (banderas CLI o configuración).<br>• Genera fragmentos que nunca exceden el `chunk_size` en caracteres o tokens.<br>• Aplica la superposición de forma consistente entre fragmentos consecutivos. |
| El código demuestra la creación adecuada de embeddings con metadatos | • Llama a un modelo de embedding de OpenAI para vectorizar cada fragmento.<br>• Almacena metadatos por fragmento que incluyen al menos la fuente/ruta del archivo y la misión (Apollo 11, Apollo 13, Challenger).<br>• Maneja documentos no nuevos según el modo `--update-mode` con una de las opciones: `skip`, `update` o `replace`. |
| Guardar e inspeccionar una colección de ChromaDB | • Guarda los embeddings en una colección de ChromaDB en el directorio `--chroma-dir` y con el nombre `--collection-name` configurados.<br>• `--stats-only` (o equivalente) imprime el tamaño de la colección y al menos un agregado (por ejemplo, número de documentos/fragmentos). |

## Integración de recuperación y LLM

| Criterios | Requisitos de entrega |
|---|---|
| El código demuestra recuperación semántica de ChromaDB | • Se conecta al backend de ChromaDB y realiza consultas de similitud usando el embedding de consulta del usuario.<br>• Devuelve los resultados top-k con k configurable en tiempo de ejecución.<br>• (Si se selecciona filtrado por misión) restringe los resultados a la misión elegida mediante filtrado por metadatos. |
| El código demuestra una construcción limpia del contexto para el LLM | • Formatea los fragmentos recuperados en una única cadena de contexto con separadores claros y atribuciones de fuente.<br>• Elimina duplicados u ordena por puntuación para evitar fragmentos repetidos. |
| El código demuestra un mensaje del sistema bien delimitado y una gestión adecuada de la conversación | • Implementa un mensaje del sistema que posiciona al asistente como un experto en misiones de la NASA que cita las fuentes recuperadas.<br>• Mantiene el historial de conversación a lo largo de los turnos (rol + contenido por turno) e incluye solo el contexto necesario para cada llamada. |
| Genera respuestas del LLM fundamentadas en el contexto recuperado | • Envía al LLM el contexto construido junto con la consulta del usuario y devuelve una respuesta.<br>• Evita afirmaciones sin fundamento al instruir al modelo para que se base en el contexto proporcionado e indique incertidumbre cuando el contexto sea insuficiente. |

## Evaluación en tiempo real

| Criterios | Requisitos de entrega |
|---|---|
| El código demuestra la integración de métricas RAGAS | • Calcula al menos la relevancia de la respuesta y la fidelidad para cada respuesta.<br>• Admite métricas adicionales (por ejemplo, BLEU, ROUGE, precisión) según lo documentado. |
| Evalúa un triple (pregunta, contexto, respuesta) | • Acepta entradas (pregunta, contexto recuperado, respuesta del modelo) y devuelve un resultado estructurado con nombres y valores de métricas.<br>• Maneja entradas vacías o mal formadas con un mensaje de error claro (sin que se produzcan fallos). |
| Evaluación por lotes usando un conjunto de prueba | • Carga preguntas de prueba (por ejemplo, `test_questions.json` o `evaluation_dataset.txt`) y calcula métricas de extremo a extremo.<br>• Genera un resumen por pregunta y un agregado (media o distribución) para cada métrica. |
| Conjunto de datos de evaluación | • Incluye `evaluation_dataset.txt` o `test_questions.json` con al menos 5 preguntas relevantes para la misión que abarquen múltiples categorías (resumen, emergencia, análisis de desastres, tripulación, técnico y cronología).<br>• El archivo se carga sin errores y se menciona en el flujo de evaluación o en el README. |
