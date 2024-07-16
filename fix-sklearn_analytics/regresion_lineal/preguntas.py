"""
Regresión Lineal Univariada
-----------------------------------------------------------------------------------------

En este laboratio se construirá un modelo de regresión lineal univariado.

"""
import numpy as np
import pandas as pd


def pregunta_01():
    """
    En este punto se realiza la lectura de conjuntos de datos.
    Complete el código presentado a continuación.
    """
    df = pd.read_csv("gm_2008_region.csv")
    y = df["life"].array
    X = df["fertility"].array
    print(y.shape)
    print(X.shape)
    y_reshaped = y.reshape(len(y), 1)
    X_reshaped = X.reshape(len(X), 1)
    print(y_reshaped.shape)
    print(X_reshaped.shape)

def pregunta_02():
    """
    En este punto se realiza la impresión de algunas estadísticas básicas
    Complete el código presentado a continuación.
    """
    df = pd.read_csv("gm_2008_region.csv")
    print(df.shape)
    print(round(df["life"].corr(df["fertility"]),4))
    print(round(df["life"].mean(),4))
    print(type(df["fertility"]))
    print(round(df["GDP"].corr(df["life"]),4))


def pregunta_03():
    """
    Entrenamiento del modelo sobre todo el conjunto de datos.
    Complete el código presentado a continuación.
    """
    from sklearn.linear_model import LinearRegression
    
    df = pd.read_csv("gm_2008_region.csv")
    X_fertility = np.array(df["fertility"]).reshape(len(df[
    y_life = np.array(df["life"]).reshape(len(df["life"]),1)
        
    reg = LinearRegression()

    prediction_space = np.linspace(
        min(X_fertility),
        max(X_fertility),
    ).reshape(50, 1)

    reg.fit(X_fertility, y_life)

    y_pred = reg.predict(prediction_space)

    print(reg.score(X_fertility, y_life).round(4))


def pregunta_04():
    """
    Particionamiento del conjunto de datos usando train_test_split.
    Complete el código presentado a continuación.
    """
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error

    df = pd.read_csv("gm_2008_region.csv")

    X_fertility = np.array(df["fertility"]).reshape(len(df["fertility"]),1)

    y_life = np.array(df["life"]).reshape(len(df["life"]),1)

    (X_train, X_test, y_train, y_test,) = train_test_split(
        X_fertility,
        y_life,
        test_size=0.2,
        random_state=53,
    )

    linearRegression = LinearRegression()

    linearRegression.fit(X_train, y_train)

    y_pred = linearRegression.predict(X_test)

    print("R^2: {:6.4f}".format(linearRegression.score(X_test, y_test)))
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("Root Mean Squared Error: {:6.4f}".format(rmse))
