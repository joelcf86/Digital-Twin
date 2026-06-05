# 🧠 Digital Twin System

Sistema de Digital Twin para monitoreo, simulación y representación virtual de procesos físicos en tiempo real.

---

## 📋 Requisitos

`pip install numpy opencv-python flask paho-mqtt`

## 🏗️ Estructura del Proyecto

```

.
├── main.py               # Punto de entrada del sistema
├── config.py            # Configuración general del sistema
├── mqtt_client.py       # Comunicación con broker MQTT
├── sensors/             # Simulación o lectura de sensores
│   ├── sensor_temp.py
│   └── sensor_hum.py
├── digital_twin/        # Núcleo del Digital Twin
│   ├── model.py
│   ├── sync.py
│   └── engine.py
├── dashboard/           # Interfaz (web o local)
│   ├── app.py
│   └── templates/
├── utils/               # Funciones auxiliares
├── data/                # Datos en tiempo real / históricos
├── logs/                # Registros del sistema
└── README.md

```

## 🚀 Instrucciones de Uso

- `1` Clonar repositorio:
`git clone https://github.com/joelcf86/Digital-Twin.git`
`cd Digital-Twin`

- `2` Instalar dependencias:
`pip install -r requirements.txt`

- `3` Configurar sistema en config.py

- `4` Ejecutar:
`python main.py`

- `5` Dashboard:
http://localhost:8000

---

## 🔄 Arquitectura

- Captura de datos (sensores)
- Comunicación MQTT
- Modelo Digital Twin
- Dashboard visual
- Almacenamiento histórico

---

## ⚙️ MQTT

`mosquitto -v`

`mosquitto_pub -t sensors/data -m "25,60"`

---

## 📈 Extensiones

- Node-RED
- InfluxDB / MySQL
- React dashboard
- IA predictiva
- Integración hardware

---

## ⚠️ Problemas

- MQTT no conecta: revisa broker
- Dashboard no abre: revisa puerto 8000
- Datos incorrectos: revisa formato MQTT

---

## 🧠 Tecnologías

Python, MQTT, Flask, NumPy

---

## 🎓 Flujo

git clone repo
cd Digital-Twin
pip install -r requirements.txt
python main.py

---

## 🚀 Objetivo

Digital Twin en tiempo real para sistemas IoT e industria 4.0
