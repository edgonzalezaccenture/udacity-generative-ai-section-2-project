# Configuración del entorno

## Entorno del proyecto

Aquí tienes un desglose del entorno técnico que utilizarás en este proyecto.

### Lenguaje de programación

- **Python:** todo el código que escribirás para este proyecto será en Python.

### Bibliotecas y SDKs clave

Usarás varios SDKs clave para interactuar con los diferentes servicios y componentes de tu sistema RAG:

- **SDK de Python de OpenAI:** esta es la biblioteca oficial para interactuar con la API de OpenAI. La usarás para acceder a los modelos de incrustación (para convertir texto en vectores) y a los modelos de completado para chat que generarán las respuestas finales.
- **Chroma SDK:** esta biblioteca te permite trabajar con ChromaDB, la base de datos vectorial de código abierto que usarás para almacenar y consultar las incrustaciones de tus documentos. La usarás para construir tu índice de documentos y realizar búsquedas semánticas.
- **RAGAS SDK:** este es el SDK que usarás para evaluar el rendimiento de tu sistema RAG. Proporciona las funciones necesarias para calcular métricas como fidelidad, relevancia de la respuesta y precisión contextual.

## Instrucciones para la máquina local

Si deseas trabajar en este proyecto en tu propia computadora, aquí tienes las instrucciones para configurar todo lo necesario.

### Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente:

- Python 3.10 o una versión más reciente instalada.
- Una clave API activa de OpenAI. Las instrucciones para obtener una clave API de OpenAI con presupuesto están en las páginas siguientes.
- Clona el repositorio de GitHub del proyecto desde: (enlace).

> El enlace al repositorio de GitHub del proyecto no venía en el texto copiado del curso.

### Pasos de instalación

Instala las bibliotecas requeridas: todas las bibliotecas de Python que necesitas están listadas en el archivo `requirements.txt`. Puedes instalarlas todas con un solo comando usando pip:

```bash
pip install -r requirements.txt
```

## Instrucciones del entorno de trabajo

En las páginas siguientes encontrarás un entorno de trabajo de Udacity donde podrás construir y ejecutar tu proyecto.
