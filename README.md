# 🤖 Asistente Virtual por Telegram - MVP

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
├── main.py                 # Archivo principal del servidor FastAPI
├── config.py               # Carga segura de variables sensibles
├── contexto_negocio.txt    # Base de conocimiento del negocio
├── bot_log.log             # Archivo de log (ignorado en Git)
├── .env                    # (ignorado por Git)
├── .gitignore              # Archivos excluidos del control de versiones

---

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

 🧑‍💻 Autor
	•	Ivan Molina
	•	GitHub: @imolina29
