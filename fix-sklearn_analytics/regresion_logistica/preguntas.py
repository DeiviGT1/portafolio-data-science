import pandas as pd


def pregunta_01():
    """
    En esta función se realiza la carga de datos.
    """
    df = pd.read_csv("mushrooms.csv")
    df = df.drop("veil-type", axis =1)
    y = df["type"]
    X = df.copy()
    X = X.drop("type", axis =1)

     return X, y


def pregunta_02():
    """
    Preparación del dataset.
    """
    from sklearn.model_selection import train_test_split

    X, y = pregunta_01()
    (X_train, X_test, y_train, y_test,) = train_test_split(
        X,
        y,
        test_size=50,
        random_state=123,
    )
     
    return X_train, X_test, y_train, y_test


def pregunta_03():
    """
    Especificación y entrenamiento del modelo. En sklearn, el modelo de regresión
    logística (a diferencia del modelo implementado normalmente en estadística) tiene
    un hiperparámetro de regularición llamado `Cs`. Consulte la documentación.

    Para encontrar el valor óptimo de Cs se puede usar LogisticRegressionCV.

    Ya que las variables explicativas son literales, resulta más conveniente usar un
    pipeline.
    """
    from sklearn.linear_model import LogisticRegressionCV
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.pipeline import Pipeline

    X_train, X_test, y_train, y_test = pregunta_02()
    pipeline = Pipeline(
        steps=[
            ("OneHotEncoder", OneHotEncoder()),
            ("LogisticRegressionCV", LogisticRegressionCV(Cs=10)),
        ],
    )
    pipeline.fit(X_train, y_train)

    return pipeline


def pregunta_04():
    """
    Evalue el modelo obtenido.
    """
    from sklearn.metrics import confusion_matrix
     
    pipeline = pregunta_03()
    X_train, X_test, y_train, y_test = pregunta_02()
    cfm_train = confusion_matrix(
        y_true=y_train,
        y_pred=pipeline.predict(X_train),
    )
    cfm_test = confusion_matrix(
        y_true=y_test,
        y_pred=pipeline.predict(X_test),
    )

    return cfm_train, cfm_test
