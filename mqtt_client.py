import pickle
import numpy as np
import json
import paho.mqtt.client as mqtt

# ---------------- MODELO ----------------
with open("fault_detector.pkl", "rb") as f:
    model_data = pickle.load(f)

fault_model = model_data["model"]
fault_scaler = model_data["scaler"]

# ---------------- ESTADO GLOBAL ----------------
latest_data = {
    "temperature": 0,
    "humidity": 0,
    "position": 0,
    "fault_type": "NONE",
    "confidence": 0.0
}

# ---------------- PREDICCIÓN ----------------
def predict_fault(temperature, humidity, position):

    X = np.array([[temperature, humidity, position]])
    X = fault_scaler.transform(X)

    fault = fault_model.predict(X)[0]

    confidence = float(
        np.max(fault_model.predict_proba(X)[0])
    )

    return fault, confidence


# ---------------- MQTT CONFIG ----------------
MQTT_BROKER = "localhost"
MQTT_TOPIC = "esp32/sensors"


# ---------------- CALLBACK MQTT ----------------
def on_message(client, userdata, msg):

    global latest_data

    try:
        data = json.loads(msg.payload.decode())

        temperature = data.get("temperature", 0)
        humidity = data.get("humidity", 0)

        # IMPORTANTE: tu encoder es position
        position = data.get("position", 0)

        fault, confidence = predict_fault(
            temperature,
            humidity,
            position
        )

        latest_data = {
            "temperature": temperature,
            "humidity": humidity,
            "position": position,
            "fault_type": fault,
            "confidence": confidence
        }

    except Exception as e:
        print("Error MQTT:", e)


# ---------------- START MQTT ----------------
client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

client.loop_start() 