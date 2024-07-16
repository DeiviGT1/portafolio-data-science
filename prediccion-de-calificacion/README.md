# 🚗 Descripción del Proyecto 🚗

Este proyecto se centra en el procesamiento y análisis de datos relacionados con despachos de artículos y su maestro, con el objetivo de preparar los datos para su uso en modelos de machine learning. Incluye scripts para la preparación de datos, entrenamiento de modelos y generación de predicciones.

## 📁 Archivos del Proyecto 📁

### 1. `data_preparation.py` 🛠️

Este script se encarga de preparar los datos relacionados con los despachos de artículos y su maestro. Contiene funciones para consultas SQL, limpieza y transformación de datos en DataFrames de Pandas, y combinación de datos de diferentes fuentes.

### 2. `data_processing.py` 🔄

El script `data_processing.py` se encarga de preparar los datos para su uso en modelos de machine learning. Contiene funciones para filtrar datos, dividirlos en conjuntos de entrenamiento y prueba, y crear pipelines de procesamiento de datos para su posterior utilización en el entrenamiento de modelos.

### 3. `model.py` 🤖

Este script se centra en el entrenamiento de modelos de machine learning utilizando diferentes clasificadores. Se encarga de cargar los datos preparados, entrenar los modelos y generar predicciones para un conjunto específico de datos, con el fin de facilitar la toma de decisiones basadas en el análisis de los resultados obtenidos.

## 🚀 Ejecución del Proyecto 🚀

Para ejecutar el proyecto, sigue estos pasos:

1. Asegúrate de tener instaladas todas las dependencias necesarias. Puedes instalarlas utilizando el siguiente comando:
  pip install -r requirements.txt

2. Ejecuta los scripts en el siguiente orden:

   - `data_preparation.py`
   - `data_processing.py`
   - `model.py`

Asegúrate de ajustar los parámetros necesarios en el archivo `model.py` antes de ejecutarlo.

## 📦 Dependencias 📦

El proyecto utiliza las siguientes dependencias:

- `scikit-learn`: Para el preprocesamiento de datos y entrenamiento de modelos de machine learning.
- `pandas`: Para la manipulación y análisis de datos.
- `numpy`: Para operaciones numéricas.
- `sqlalchemy`: Para la conexión y consultas a bases de datos SQL.
- `openpyxl`: Para leer archivos Excel.
- `matplotlib`: Para visualización de datos.

Asegúrate de tener estas dependencias instaladas antes de ejecutar el proyecto.

## 🧠 Modelos Seleccionados 🧠

Durante el desarrollo de este proyecto, se han seleccionado tres modelos de machine learning para abordar distintos aspectos del problema:

1. **Modelo de Redes Neuronales**:
   - Las redes neuronales son conocidas por su capacidad para aprender patrones complejos en datos, lo que las hace adecuadas para una amplia gama de problemas de clasificación y regresión.
   - Pueden manejar conjuntos de datos grandes y de alta dimensionalidad, adaptándose bien a problemas con una gran cantidad de características.
   - En este caso, el modelo de redes neuronales puede ser útil si el problema es intrínsecamente complejo y no puede ser abordado eficazmente por modelos más simples como los árboles de decisión o KNN.

2. **Árboles de Decisión**:
   - Los árboles de decisión son modelos simples de entender e interpretar, lo que los hace útiles para tareas de clasificación y regresión.
   - Son robustos frente a datos ruidosos y fáciles de visualizar, lo que facilita la comprensión de cómo se toman las decisiones.
   - Los árboles de decisión son excelentes candidatos cuando se requiere una explicabilidad del modelo y se cuenta con características fácilmente interpretables.

3. **K-Nearest Neighbors (KNN)**:
   - KNN es un algoritmo simple y no paramétrico utilizado tanto para clasificación como para regresión.
   - Su enfoque se basa en la suposición de que las instancias similares tienden a estar cerca en el espacio de características.
   - KNN puede ser particularmente útil cuando la estructura subyacente de los datos es compleja y no lineal.

La elección de estos tres modelos proporciona una diversidad de enfoques que pueden complementarse entre sí para abordar diferentes aspectos y desafíos del problema. En conjunto, esta combinación de modelos ofrece flexibilidad y capacidad para abordar una variedad de escenarios en el procesamiento y análisis de datos relacionados con despachos de artículos y su maestro.


## 📊 Evaluación de Resultados: Matriz de Confusión 📊

Para evaluar el rendimiento de los modelos de machine learning seleccionados en este proyecto, se empleó la técnica de la matriz de confusión. La matriz de confusión es una herramienta fundamental en la evaluación de modelos de clasificación, ya que proporciona una visión detallada de cómo el modelo está clasificando las instancias en diferentes clases.

La matriz de confusión organiza las predicciones del modelo en una tabla, donde las filas representan las clases reales y las columnas representan las clases predichas por el modelo. Las celdas de la matriz muestran el número de instancias clasificadas correctamente (verdaderos positivos y verdaderos negativos) y incorrectamente (falsos positivos y falsos negativos) para cada clase.

Analizar la matriz de confusión permite identificar patrones de error del modelo, como la tendencia a confundir ciertas clases entre sí, y proporciona métricas de evaluación adicionales como precisión, exhaustividad y F1-score.

La interpretación adecuada de la matriz de confusión es crucial para comprender el rendimiento del modelo y tomar decisiones informadas sobre posibles ajustes o mejoras en el proceso de entrenamiento.

En este proyecto, la matriz de confusión se utilizó como una herramienta integral para evaluar y comparar el rendimiento de los modelos de redes neuronales, árboles de decisión y K-Nearest Neighbors en la tarea de clasificación de despachos de artículos y su maestro.

## ✍️ Autor ✍️

Este proyecto fue desarrollado por [David Gonzalez](https://github.com/DeiviGT1).

