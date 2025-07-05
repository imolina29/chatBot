import pytest
from app.main import generar_respuesta
import asyncio

@pytest.mark.asyncio
async def test_generar_respuesta_basica():
    entrada = "¿Cuál es el horario de atención?"
    respuesta = await generar_respuesta(entrada)
    assert isinstance(respuesta, str)
    assert len(respuesta) > 0