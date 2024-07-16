from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_selector, ColumnTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline

from data_preparation import main

#################################################################### Descripción ########################################################################
#########################################################################################################################################################

# Este script se encarga de preparar los datos para su uso en modelos de machine learning. Contiene funciones para filtrar 
# datos, dividirlos en conjuntos de entrenamiento y prueba, y crear pipelines de procesamiento de datos para su posterior 
# utilización en el entrenamiento de modelos.


########################################################################################################################################################
########################################################################################################################################################

class DataProcessor:
    @staticmethod
    def data_final(genero=None, categoria=None, rs=10):
        # Obtener la tabla de items
        tabla_items = main()
        
        # Filtrar la tabla según el género y la categoría, si se especifican
        df = tabla_items.copy()
        if genero:
            df = df[(df['genero'] == genero)]
        if categoria:
            df = df[(df['categoria'] == categoria)]

        # Si el género es 'hombre', eliminar ciertas columnas
        if genero == 'hombre':
            df.drop(['base_tela', 'sub_categoria'], axis=1, inplace=True)
        
        # Filtrar las columnas que tienen al menos 10 datos
        df_filtrado = df.copy()
        for col in df.columns:
            conteo = df_filtrado[col].value_counts()
            filtro = conteo[conteo >= 10].index.tolist()
            df_filtrado = df_filtrado[df_filtrado[col].isin(filtro)]
        df = df_filtrado
        
        # Separar características (X) y etiquetas (y)
        X = df.drop(['calificacion', 'genero', 'categoria'], axis=1)
        y = df['calificacion']
        
        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=rs)
        
        # Devolver los conjuntos de datos divididos y los datos completos
        return X_train, X_test, y_train, y_test, X, y

    @staticmethod
    def create_pipeline(cat_encoder, model, num_encoder):
        pipeline = Pipeline([
            ('preprocessing', ColumnTransformer(
                transformers=[
                    ('encoding', cat_encoder, make_column_selector(dtype_include='object')),
                    ('num_encoding', num_encoder, make_column_selector(dtype_include='number'))
                ],
                remainder='passthrough'
            )),
            ('feature_selection', SelectKBest(score_func=chi2)),
            ('classification', model)
        ])
        return pipeline

    @staticmethod
    def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=None, normalize=False):
        """
        Función para visualizar la matriz de confusión.

        Parámetros:
        - cm: Matriz de confusión generada por sklearn.metrics.confusion_matrix
        - target_names: Nombres de las clases de clasificación
        - title: Título de la gráfica (por defecto: 'Confusion matrix')
        - cmap: Mapa de colores para la visualización de la matriz (por defecto: None)
        - normalize: Booleano para indicar si se debe normalizar la matriz (por defecto: False)
        """

        import matplotlib.pyplot as plt  # Importa matplotlib para visualización
        import numpy as np  # Importa numpy para cálculos numéricos
        import itertools  # Importa itertools para operaciones de iteración

        # Cálculo de la precisión y tasa de clasificación errónea
        accuracy = np.trace(cm) / float(np.sum(cm))
        misclass = 1 - accuracy

        # Si no se proporciona un mapa de colores, usa el mapa de colores 'Blues'
        if cmap is None:
            cmap = plt.get_cmap('Blues')

        # Crea una figura y ejes para dos subgráficos
        fig, ax = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'hspace': 0.5})

        # Plotear la matriz de confusión en el primer subgráfico
        im = ax[0].imshow(cm, interpolation='nearest', cmap=cmap)
        fig.colorbar(im, ax=ax[0])  # Añade una barra de colores

        # Plotear la matriz de confusión normalizada en el segundo subgráfico
        im_norm = ax[1].imshow(cm, interpolation='nearest', cmap=cmap)
        fig.colorbar(im_norm, ax=ax[1])  # Añade una barra de colores

        # Si se proporcionan nombres de clases, establece las marcas de los ejes
        if target_names is not None:
            tick_marks = np.arange(len(target_names))
            ax[0].set_xticks(tick_marks, target_names, rotation=45)
            ax[0].set_yticks(tick_marks, target_names)
            ax[1].set_xticks(tick_marks, target_names, rotation=45)
            ax[1].set_yticks(tick_marks, target_names)

        # Normaliza la matriz de confusión
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        # Define umbrales para resaltar valores
        thresh = cm.min() + (cm.max() - cm.min()) / 2
        thresh_norm = cm_norm.min() + (cm_norm.max() - cm_norm.min()) / 2

        # Añade texto con los valores de la matriz en el primer subgráfico
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            ax[0].text(j, i, "{:,}".format(cm[i, j]),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")

        # Añade texto con los valores normalizados en el segundo subgráfico
        for i, j in itertools.product(range(cm_norm.shape[0]), range(cm_norm.shape[1])):
            ax[1].text(j, i, "{:0.2f}%".format(cm_norm[i, j]),
                    horizontalalignment="center",
                    color="white" if cm_norm[i, j] > thresh_norm else "black")

        # Etiquetas de los ejes y título para el primer subgráfico
        ax[0].set_ylabel('True label')
        ax[0].set_xlabel('Predicted label')

        # Etiquetas de los ejes y título para el segundo subgráfico
        ax[1].set_ylabel('True label')
        ax[1].set_xlabel('Predicted label')

        # Título de la figura con la precisión y tasa de error
        fig.suptitle('Accuracy={:0.2f}% \nMisclass={:0.2f}%'.format(accuracy, misclass), fontsize=14, color='Black')

        plt.tight_layout()  # Ajusta el diseño de la gráfica
        plt.show()  # Muestra la gráfica