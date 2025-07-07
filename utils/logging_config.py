# utils/logging_config.py
import logging

def configurar_logs():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("bot_log.log", encoding="utf-8")
        ]
    )