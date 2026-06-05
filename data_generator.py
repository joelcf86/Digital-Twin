import pandas as pd
import numpy as np

# Reproducibilidad
np.random.seed(42)

datos = []

NUM_REGISTROS = 2000

for _ in range(NUM_REGISTROS):

    # Variables de entrada
    temperature = round(
        np.random.uniform(20, 60),
        2
    )

    humidity = round(
        np.random.uniform(30, 95),
        2
    )

    position = np.random.randint(
        0,
        1000
    )

    # Detección de condiciones anormales
    overheat = temperature > 45
    high_humidity = humidity > 80
    position_error = (
        position < 100
        or
        position > 900
    )

    fault_count = sum([
        overheat,
        high_humidity,
        position_error
    ])

    # Clasificación
    if fault_count == 0:

        system_status = "OK"
        fault_type = "NONE"

    elif fault_count > 1:

        system_status = "WARNING"
        fault_type = "MULTIPLE_FAULTS"

    elif overheat:

        system_status = "WARNING"
        fault_type = "OVERHEAT"

    elif high_humidity:

        system_status = "WARNING"
        fault_type = "HIGH_HUMIDITY"

    else:

        system_status = "WARNING"
        fault_type = "POSITION_ERROR"

    datos.append([
        temperature,
        humidity,
        position,
        system_status,
        fault_type
    ])

# Crear DataFrame
df = pd.DataFrame(
    datos,
    columns=[
        "temperature",
        "humidity",
        "position",
        "system_status",
        "fault_type"
    ]
)

# Guardar CSV
df.to_csv(
    "sensor_data.csv",
    index=False
)

print("\nPrimeras filas:")
print(df.head())

print("\nResumen:")
print(df["system_status"].value_counts())

print("\nTipos de falla:")
print(df["fault_type"].value_counts())

print("\nArchivo generado correctamente:")
print("sensor_data.csv")