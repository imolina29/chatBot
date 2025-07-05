from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

token = os.getenv("TELEGRAM_TOKEN")
print("Valor sin repr:", token)
print("Valor repr:", repr(token))
print("Contiene ':'?", ':' in token)