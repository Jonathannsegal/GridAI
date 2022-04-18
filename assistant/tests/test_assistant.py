import os
from assistant.src.app import *
from assistant.src.speech_to_text import *
from assistant.src.app import app
import pytest


@pytest.fixture
def client():
    """Pytest client fixture"""
    with app.test_client() as client:
        yield client

def test_speech():
    """speech to text test"""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
        os.getcwd() + "/assistant/client_secret/speechtotext-331119-820cdd23000d.json"
    assert speech_text("gs://cloud-samples-data/speech/brooklyn_bridge.raw", True) \
         == "how old is the Brooklyn Bridge"
    assert speech_text(os.getcwd() + "/assistant/test_voice_files/house/0a7c2a8d_nohash_0.wav",
                       False) == "house"

def test_text_request(client):
    """Tests a text request sent to the Assistant"""
    ret = client.post(
        '/text',
        json={
            "text": "Show voltages less than 100",
        }
    )
    assert ret.status_code == 200

def test_app_speech():
    """Test voice_to_text in app"""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
        os.getcwd() + "/assistant/client_secret/speechtotext-331119-820cdd23000d.json"
    assert voice_to_text(os.getcwd() + "/assistant/test_voice_files/house/0a7c2a8d_nohash_0.wav")\
         == "house"

def test_allowed_file():
    """Test allowed extensions"""
    assert allowed_file("abc.wav")
    assert not allowed_file("abc.png")
