# Resumen del proyecto

## Tu misión: construir un sistema de chat de inteligencia para la NASA

En este proyecto, te pondrás en el lugar de un especialista en operaciones de misión de la NASA. Tu tarea es construir un sistema de preguntas y respuestas que pueda responder consultas sobre algunas de las misiones espaciales más históricas de la NASA. Trabajarás con transcripciones reales de misiones y documentos técnicos de Apollo 11, Apollo 13 y las misiones del Challenger.

El objetivo es crear una herramienta que permita a astronautas, investigadores o incluso a un historiador curioso hacer una pregunta en inglés sencillo —como «¿Qué problemas enfrentó el Apollo 13?»— y obtener una respuesta precisa y detallada basada directamente en los archivos oficiales de la NASA.

Para lograr esto, vas a construir un sistema completo de generación aumentada por recuperación (RAG).

## El plan del proyecto

Trabajarás con una serie de archivos Python, cada uno con una función específica.

Aquí tienes una visión general de lo que construirás, paso a paso:

1. **El pipeline de incrustación.** Primero, tomarás todos esos archivos de texto sin procesar de la NASA y los procesarás. Escribirás código para dividirlos en fragmentos más pequeños y manejables, luego convertirás esos fragmentos en representaciones numéricas —los embeddings— y los almacenarás en ChromaDB.
2. **El cliente RAG.** Este es el núcleo de tu sistema de recuperación. Construirás la lógica que toma la pregunta del usuario, busca en la base de datos ChromaDB los fragmentos de documentos más relevantes y luego formatea esa información de manera ordenada para usarla como contexto.
3. **El cliente LLM.** Aquí te conectarás con la API de OpenAI. Este componente tomará la pregunta del usuario y el contexto de tu cliente RAG para generar una respuesta útil y legible por humanos.
4. **El evaluador RAGAS.** ¿Cómo sabes si tu sistema RAG funciona bien? Implementarás un sistema de evaluación en tiempo real usando RAGAS.
5. **La aplicación de chat.** Finalmente, juntarás todo en una interfaz de chat interactiva usando Streamlit.

## Lo que podrás hacer después

Cuando termines, habrás construido una aplicación de IA completa y funcional. Habrás demostrado un conjunto valioso de habilidades, incluyendo:

- Construir un sistema RAG de extremo a extremo.
- Usar bases de datos vectoriales como ChromaDB para búsqueda semántica.
- Integrar y diseñar indicaciones para modelos de lenguaje grandes para tareas específicas.
- Evaluar el rendimiento de un sistema de IA con herramientas modernas.

Este proyecto es una pieza fantástica para añadir a tu portafolio. ¿Listo para comenzar?

## Evaluación del proyecto

Tu proyecto será evaluado por mentores utilizando una rúbrica detallada. En las páginas siguientes encontrarás la rúbrica; familiarízate con ella. Asegúrate de revisar tu proyecto según sus criterios antes de enviarlo.
