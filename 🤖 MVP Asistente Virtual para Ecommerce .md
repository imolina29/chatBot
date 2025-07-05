🤖 MVP Asistente Virtual para Ecommerce vía Telegram

Este proyecto es un MVP gratuito para crear un asistente virtual personalizado para pequeños y medianos ecommerce usando:
	•	Telegram como canal de mensajería.
	•	OpenAI para generar respuestas inteligentes.
	•	FastAPI como backend ligero.
	•	Archivos .txt como fuente de contexto (simulando una base de conocimiento).

⸻

✅ Características principales
	•	Recibe mensajes desde Telegram y responde automáticamente.
	•	Incluye un contexto editable del negocio.
	•	Logs en tiempo real (con rotación y seguimiento).
	•	Configuración fácil mediante variables de entorno y script automático de webhook.

⸻

🚀 Tecnologías utilizadas
	•	Python 3.10+
	•	FastAPI
	•	OpenAI GPT-3.5
	•	Telegram Bot API
	•	Uvicorn
	•	Ngrok (para exponer tu API local a Telegram)

⸻

🛠️ Instrucciones de instalación

1. Clona el repositorio

git clone <url-del-repo>
cd <nombre-del-repo>

2. Instala las dependencias

pip install -r requirements.txt

3. Crea el archivo .env

TELEGRAM_TOKEN=TU_TOKEN_DEL_BOT
OPENAI_API_KEY=TU_API_KEY_OPENAI

4. Crea el archivo de contexto personalizado

# contexto_negocio.txt
- Vendemos ropa para hombres y mujeres.
- Tenemos envío gratis desde $50.
- Aceptamos pagos con tarjeta, transferencia y contra entrega.
- Cambios y devoluciones hasta 10 días.
- WhatsApp: +123456789

5. Inicia el servidor FastAPI

uvicorn main:app --reload --port 8000

6. Abre ngrok en otro terminal

ngrok http 8000

Copia la URL pública generada por ngrok (ej: https://xxxxx.ngrok-free.app)

7. Configura el webhook

Edita el main.py y en la función configurar_webhook() reemplaza la URL por la que generó ngrok. Luego en consola:

python -c "from main import configurar_webhook; configurar_webhook()"


⸻

📡 Verificar si todo funciona
	1.	Entra al chat con tu bot en Telegram
	2.	Envía un mensaje como “¿Qué formas de pago tienen?”
	3.	El bot responderá usando el contexto cargado.

⸻

📄 Visualizar logs en tiempo real

Opción 1: Consola Linux/macOS

tail -f bot_log.log

Opción 2: PowerShell en Windows

Get-Content .\bot_log.log -Wait

Opción 3: Python (visor integrado)

python -c "

# App principal
fastapi==0.110.0
uvicorn[standard]==0.29.0
requests==2.31.0
python-dotenv==1.0.1
openai==1.30.1

# Pruebas
pytest==8.4.1
pytest-asyncio==0.23.7
anyio==4.3.0

# Opcional para desarrollo (logs más detallados, etc.)
httpx==0.27.0