# 🤖 Asistente Virtual por Telegram - MVP
# 🤖 Chatbot con IA y lógica híbrida

Este es un **bot de asistencia virtual gratuito** desarrollado como MVP (Producto Mínimo Viable) para responder preguntas de clientes usando inteligencia artificial.

## 🚀 Tecnologías utilizadas

- **FastAPI**: para el backend web (manejo de webhooks)
- **Telegram Bot**: canal de entrada/salida con usuarios
- **OpenAI (GPT-3.5)**: generación de respuestas personalizadas
- **ChromaDB (opcional)**: para contexto con RAG
- **Ngrok**: exposición del servidor local para desarrollo
- **Python 3.10+**

---

## 📁 Estructura del Proyecto
virtual_assistance/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── telegram.py          ← Aquí llega el webhook
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bot.py               ← Lógica del bot (envío, manejo comandos)
│   │   ├── telegram.py          ← Funciones directas para Telegram API (si usas requests)
│   │   └── history.py           ← Guardado de conversación
│   ├── config/
│   │   ├── __init__.py
│   │   └── constants.py         ← ASESOR_CHAT_ID u otras constantes
│   └── utils/
│       ├── __init__.py
│       └── conversaciones.py    ← Manejo de sesiones de chat y reenvío
├── requirements.txt
└── env/                         ← Tu entorno virtual (ignorado por git)

## 🛠️ Configuración inicial

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
ngrok http 8000
from main import configurar_webhook
configurar_webhook()

✅ Funcionalidades
	•	🔐 Variables sensibles protegidas con .env
	•	🔄 Manejo automático del webhook con ngrok
	•	📉 Detección automática de créditos agotados en OpenAI
	•	📩 Envío de alerta al administrador si el bot falla por créditos
	•	⚠️ Suspensión temporal automática del bot
	•	🧠 Contexto personalizado desde contexto_negocio.txt
	•	🧼 Código limpio, modular y optimizado para producción

Mejoras 
# app/services/bot.py

1. 📦 Imports y configuración inicial
2. 🧱 Funciones utilitarias
   - enviar_mensaje()
   - notificar_error()
3. 🤖 Comandos del bot (manejar_comando)
4. 🔁 Funciones auxiliares del bot (normalizar, validaciones)

 🧑‍💻 Autor
	•	Ivan Molina
	•	GitHub: @imolina29
