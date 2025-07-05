from app.main import enviar_mensaje_telegram
import pytest

def test_enviar_mensaje_telegram_mock(monkeypatch):
    def mock_post(url, json):
        class MockResponse:
            status_code = 200
            def json(self): return {"ok": True}
        return MockResponse()

    import requests
    monkeypatch.setattr(requests, "post", mock_post)

    try:
        enviar_mensaje_telegram(123456789, "Mensaje de prueba")
    except Exception:
        pytest.fail("enviar_mensaje_telegram lanzó una excepción")