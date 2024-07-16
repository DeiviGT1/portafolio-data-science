"""
Análisis de Sentimientos usando Naive Bayes
-----------------------------------------------------------------------------------------

El archivo `amazon_cells_labelled.txt` contiene una serie de comentarios sobre productos
de la tienda de amazon, los cuales están etiquetados como positivos (=1) o negativos (=0)
o indterminados (=NULL). En este taller se construirá un modelo de clasificación usando
Naive Bayes para determinar el sentimiento de un comentario.

"""
import numpy as np
import pandas as pd


def pregunta_01():
    """
    Carga de datos.
    -------------------------------------------------------------------------------------
    """

    # Lea el archivo `amazon_cells_labelled.tsv` y cree un DataFrame usando pandas.
    # Etiquete la primera columna como `msg` y la segunda como `lbl`. Esta función
    # retorna el dataframe con las dos columnas.
    df = pd.read_csv("./amazon_cells_labelled.tsv", 
            sep="\t", 
            header=None, 
            names=["msg", "lbl"])

    # Separe los grupos de mensajes etiquetados y no etiquetados.
    df_tagged = df[df["lbl"].notnull()]
    df_untagged = df[df["lbl"].isnull()]

    x_tagged = df_tagged["msg"]
    y_tagged = df_tagged["lbl"]

    x_untagged = df_untagged["msg"]
    y_untagged = df_untagged["lbl"]

    # Retorne los grupos de mensajes
    return x_tagged, y_tagged, x_untagged, y_untagged


def pregunta_02():
    """
    Preparación de los conjuntos de datos.
    -------------------------------------------------------------------------------------
    """

    # Importe train_test_split
    from sklearn.model_selection import train_test_split

    # Cargue los datos generados en la pregunta 01.
    x_tagged, y_tagged, x_untagged, y_untagged = pregunta_01()

    # Divida los datos de entrenamiento y prueba. La semilla del generador de números
    # aleatorios es 12345. Use el 10% de patrones para la muestra de prueba.
    x_train, x_test, y_train, y_test = train_test_split(
        x_tagged,
        y_tagged,
        test_size= 0.1,
        random_state= 12345,
    )

    # Retorne `X_train`, `X_test`, `y_train` y `y_test`
    return x_train, x_test, y_train, y_test


def pregunta_03():
    """
    Construcción de un analizador de palabras
    -------------------------------------------------------------------------------------
    """
    # Importe el stemmer de Porter
    # Importe CountVectorizer
    from nltk.stem import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer


    # Cree un stemeer que use el algoritmo de Porter.
    stemmer = PorterStemmer()

    # Cree una instancia del analizador de palabras (build_analyzer)
    analyzer = CountVectorizer().build_analyzer()

    # Retorne el analizador de palabras
    return lambda x: (stemmer.stem(w) for w in analyzer(x))


def pregunta_04():
    """
    Especificación del pipeline y entrenamiento
    -------------------------------------------------------------------------------------
    """
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.model_selection import GridSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.naive_bayes import BernoulliNB

    x_train, x_test, y_train, y_test = pregunta_02()
    analyzer = pregunta_03()
    countVectorizer = CountVectorizer(
        analyzer=analyzer,
        lowercase=True,
        stop_words="english",
        token_pattern="word",
        binary=True,
        max_df=1.0,
        min_df=5,
    )
    pipeline = Pipeline(
        steps=[
            ("countVectorizer", countVectorizer),
            ("BernoulliNB", BernoulliNB()),

        ],
    )
    param_grid = {
        "BernoulliNB__alpha": np.arange(0.1, 1.1, 0.1),
    }
    gridSearchCV = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="accuracy",
    )
    gridSearchCV.fit(x_train, y_train)

    return gridSearchCV

def pregunta_05():
    """
    Evaluación del modelo
    -------------------------------------------------------------------------------------
    """
    from sklearn.metrics import confusion_matrix
    
    gridSearchCV = pregunta_04()
    X_train, X_test, y_train, y_test = pregunta_02()
    cfm_train = confusion_matrix(
        y_true=y_train,
        y_pred=gridSearchCV.predict(X_train),
    )

    cfm_test = confusion_matrix(
        y_true=y_test,
        y_pred=gridSearchCV.predict(X_test),
    )
    
    return cfm_train, cfm_test


def pregunta_06():
    """
    Pronóstico
    -------------------------------------------------------------------------------------
    """
    gridSearchCV = pregunta_04()
    x_tagged, y_tagged, x_untagged, y_untagged = pregunta_01()
    y_untagged_pred = gridSearchCV.predict(x_untagged)

    return y_untagged_pred
