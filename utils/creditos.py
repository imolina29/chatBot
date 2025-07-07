# utils/creditos.py

import requests
import logging
from app.config import OPENAI_API_KEY

def obtener_creditos_openai() -> str:
    url = "https://api.openai.com/dashboard/billing/credit_grants"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        total = data.get("total_granted", 0)
        usado = data.get("total_used", 0)
        restante = data.get("total_available", 0)

        porcentaje_usado = (usado / total) * 100 if total else 0
        return (
            f"💰 Créditos disponibles: {restante:.2f} USD\n"
            f"🔋 Porcentaje usado: {porcentaje_usado:.2f}%\n"
            f"📊 Total otorgado: {total:.2f} USD\n"
            f"🧾 Total usado: {usado:.2f} USD"
        )
        
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error al consultar créditos: {http_err}")
        return "❌ No se pudo obtener la información de créditos (HTTP error)."
    except Exception as err:
        logging.error(f"Error inesperado al consultar créditos: {err}")
        return "❌ No se pudo obtener la información de créditos (error inesperado)."