import pandas as pd
import numpy as np
import pickle
import warnings

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

warnings.filterwarnings("ignore")

plt.style.use("seaborn-v0_8-darkgrid")


# ==========================================
# CARGA DE DATOS
# ==========================================

def load_data(filename="sensor_data.csv"):

    df = pd.read_csv(filename)

    print("\n=================================")
    print("DATOS CARGADOS")
    print("=================================")

    print(f"Registros: {len(df)}")
    print(f"Columnas : {list(df.columns)}")

    return df


# ==========================================
# PREPARACIÓN
# ==========================================

def prepare_data(df):

    features = [
        "temperature",
        "humidity",
        "position"
    ]

    target = "fault_type"

    df = df.dropna()

    X = df[features].values
    y = df[target].values

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        features
    )


# ==========================================
# ENTRENAMIENTO
# ==========================================

def train_model(
    X_train,
    X_test,
    y_train,
    y_test,
    scaler,
    features
):

    print("\n=================================")
    print("ENTRENANDO RANDOM FOREST")
    print("=================================")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(f"\nAccuracy: {accuracy:.4f}")

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    plt.figure(figsize=(8,6))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=model.classes_,
        yticklabels=model.classes_
    )

    plt.title(
        "Matriz de Confusión"
    )

    plt.xlabel(
        "Predicción"
    )

    plt.ylabel(
        "Valor Real"
    )

    plt.tight_layout()

    plt.show()

    model_package = {

        "model": model,

        "scaler": scaler,

        "features": features,

        "classes": list(
            model.classes_
        )

    }

    with open(
        "fault_detector.pkl",
        "wb"
    ) as f:

        pickle.dump(
            model_package,
            f
        )

    print(
        "\n✓ Archivo generado: fault_detector.pkl"
    )

    return model


# ==========================================
# PRUEBA DEL MODELO
# ==========================================

def test_prediction():

    with open(
        "fault_detector.pkl",
        "rb"
    ) as f:

        data = pickle.load(f)

    model = data["model"]
    scaler = data["scaler"]

    temperatura = 52
    humedad = 88
    posicion = 950

    X = np.array([
        [
            temperatura,
            humedad,
            posicion
        ]
    ])

    X = scaler.transform(X)

    fault = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    confidence = np.max(
        probabilities
    )

    print("\n=================================")
    print("PRUEBA DEL MODELO")
    print("=================================")

    print(
        f"Temperatura : {temperatura}"
    )

    print(
        f"Humedad     : {humedad}"
    )

    print(
        f"Posición    : {posicion}"
    )

    print(
        f"Falla       : {fault}"
    )

    print(
        f"Confianza   : {confidence:.2%}"
    )


# ==========================================
# MAIN
# ==========================================

def main():

    df = load_data(
        "sensor_data.csv"
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        features
    ) = prepare_data(df)

    train_model(
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        features
    )

    test_prediction()


if __name__ == "__main__":
    main()