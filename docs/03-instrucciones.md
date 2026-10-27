# Instrucciones

Clona el repositorio de GitHub con el código inicial: [github.com/udacity/cd13318-exercises-project](https://github.com/udacity/cd13318-exercises-project/).

Aquí tienes una ruta de implementación paso a paso que puedes seguir.

## Fase 1: infraestructura básica

Esta primera fase se centra en construir los componentes fundamentales de tu sistema RAG.

### 1. Implementa el cliente LLM (`llm_client.py`)

- Aquí te conectarás con la API de OpenAI. Aprenderás cómo redactar un buen prompt del sistema para darle a la IA su «persona» como experto de la NASA. Este componente tomará la pregunta del usuario y el contexto de tu cliente RAG para generar una respuesta útil y comprensible para humanos.
- **Qué harás:** tu primer paso es crear una conexión con la API de OpenAI. Escribirás el código para enviar la pregunta del usuario, junto con cualquier contexto relevante e historial de conversación, a un LLM como GPT-3.5 o GPT-4.
- **Tareas:**
  - Definir un prompt del sistema que indique al modelo actuar como un experto de la NASA.
  - Gestionar el historial de conversación para que el modelo recuerde las interacciones previas.
  - Escribir la función que envía la solicitud a OpenAI y devuelve la respuesta del modelo.

### 2. Construye el cliente RAG (`rag_client.py`)

- Este es el núcleo de tu sistema de recuperación. Construirás la lógica que toma la pregunta del usuario, busca en la base de datos ChromaDB los fragmentos de documentos más relevantes y luego formatea esa información de manera ordenada para ser usada como contexto.
- **Qué harás:** a continuación, construirás la parte de «recuperación» del sistema RAG. Este componente es responsable de buscar en la base de datos vectorial los documentos más relevantes para responder a la pregunta del usuario.
- **Tareas:**
  - Conectarte con el backend de ChromaDB.
  - Implementar la función de búsqueda semántica que recibe una pregunta y encuentra los fragmentos de documentos que mejor coinciden.
  - Formatear los documentos recuperados en una cadena de contexto limpia que pueda ser pasada al LLM.

### 3. Crea el pipeline de embeddings (`embedding_pipeline.py`)

- Tomarás todos esos archivos de texto crudos de la NASA y los procesarás. Escribirás código para dividirlos en fragmentos más pequeños y manejables y luego convertir esos fragmentos en representaciones numéricas —o embeddings— usando un modelo de OpenAI. Luego almacenarás todo esto en una base de datos vectorial especializada llamada ChromaDB. Esta es la base de la «memoria» de tu sistema.
- **Qué harás:** esta es la parte más extensa de la configuración. Escribirás un script que tome todos los archivos `.txt` crudos de la NASA, los procese, cree embeddings y los guarde en la base de datos ChromaDB.
- **Tareas:**
  - Implementar una estrategia de segmentación de texto para dividir documentos grandes en partes más pequeñas y manejables.
  - Usar la API de OpenAI para generar embeddings para cada fragmento de texto.
  - Gestionar la creación y población de colecciones dentro de ChromaDB.
  - Construir una interfaz de línea de comandos para que puedas ejecutar fácilmente este pipeline desde tu terminal.

## Fase 2: evaluación e interfaz

Una vez construido el sistema básico, te enfocarás en evaluar su rendimiento y crear una interfaz amigable para el usuario.

### 4. Desarrolla el evaluador RAGAS (`ragas_evaluator.py`)

- ¿Cómo sabes si tu sistema RAG es bueno? Implementarás un sistema de evaluación en tiempo real usando un framework llamado RAGAS. Esto puntuará automáticamente las respuestas de tu sistema en métricas como fidelidad (¿se apega a los hechos?) y relevancia (¿la respuesta es realmente útil?).
- **Qué harás:** construirás el sistema que califica la calidad de las respuestas de tu sistema RAG. Esto te dará retroalimentación en tiempo real sobre la calidad de tu sistema.
- **Tareas clave:**
  - Integrar el framework RAGAS.
  - Definir las métricas de evaluación que deseas usar, como relevancia y fidelidad de la respuesta.
  - Escribir la función que recibe una pregunta, una respuesta y el contexto, y devuelve un conjunto de puntuaciones de calidad.

### 5. Construye la aplicación de chat (`chat.py`)

- Finalmente, juntarás todo en una interfaz de chat interactiva usando Streamlit. ¡Aquí es donde tu proyecto cobra vida! Los usuarios podrán seleccionar diferentes modelos, elegir una misión para enfocarse y ver las puntuaciones de evaluación de cada respuesta en tiempo real.
- **Qué harás:** integrarás todos los componentes en una única aplicación web interactiva con Streamlit.
- **Tareas:**
  - Construir la interfaz de chat donde un usuario pueda escribir preguntas.
  - Integrar todos los componentes que has construido: el cliente RAG, el cliente LLM y el evaluador RAGAS.
  - Mostrar la respuesta de la IA y sus puntuaciones de calidad en tiempo real en la interfaz.

## Evaluación del proyecto

Tu proyecto será evaluado por mentores utilizando una rúbrica detallada. En las páginas siguientes encontrarás la rúbrica. Familiarízate con ella y asegúrate de revisar tu proyecto conforme a sus criterios antes de enviarlo.

## Instrucciones para la entrega

Cuando estés listo para entregar tu proyecto, sigue estos pasos para asegurarte de que todo esté incluido.

### Lista de verificación para la entrega

1. **Implementa todos los elementos TODO:** revisa cada uno de los archivos Python (`llm_client.py`, `rag_client.py`, `embedding_pipeline.py`, `ragas_evaluator.py` y `chat.py`) y asegúrate de haber completado todos los comentarios `TODO`.
2. **Pruebas de extremo a extremo:** antes de entregar, ejecuta todo el flujo de trabajo para confirmar que todo funciona en conjunto.
   - Primero, ejecuta tu pipeline de embeddings para procesar los documentos.
   - Luego, lanza la aplicación de chat y pruébala con varias preguntas para asegurarte de que responde correctamente y muestra las puntuaciones de evaluación.
3. **Proporciona preguntas de ejemplo:** en un archivo de texto llamado `evaluation_dataset.txt`, incluye algunas preguntas de ejemplo que usaste para las pruebas y muestra las respuestas que esperabas que el sistema proporcionara.
4. **Prepara tus archivos:**
   - Asegúrate de que todo tu código esté limpio.
   - Comprime todos los archivos de tu proyecto, incluyendo tu informe, en un solo archivo.

En las páginas siguientes encontrarás un botón para la entrega, además de instrucciones para comprimir tu código y enviarlo a los mentores. Recomendamos que trabajes en un repositorio de GitHub, ya sea en el entorno de trabajo de Udacity o en tu máquina local.
