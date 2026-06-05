from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
import json
import paho.mqtt.client as mqtt

from mqtt_client import predict_fault

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- ESTADO GLOBAL ----------------
latest_data = {
    "temperature": 0,
    "humidity": 0,
    "position": 0,
    "fault_type": "NONE",
    "confidence": 0.0
}

# ---------------- MQTT CONFIG ----------------
MQTT_BROKER = "localhost"
MQTT_TOPIC = "esp32/sensors"

# ---------------- FUNCIÓN MQTT ----------------
def on_message(client, userdata, msg):
    global latest_data

    try:
        data = json.loads(msg.payload.decode())

        temperature = data.get("temperature", 0)
        humidity = data.get("humidity", 0)
        position = data.get("encoder", 0)

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
        print("MQTT ERROR:", e)

# ---------------- INICIAR MQTT ----------------
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

# ---------------- FRONTEND ----------------
@app.get("/")
async def home():
    with open("templates/index.html", encoding="utf8") as f:
        return HTMLResponse(f.read())

# ---------------- WEBSOCKET ----------------
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        await ws.send_json(latest_data)
        await asyncio.sleep(0.1)