from pathlib import Path
from unittest import mock
from assistant.src.app import *
from assistant.src.speech_to_text import *


def speech_test():
    """speech to text test"""
    mock.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": Path.cwd() / "assistant/client_secret/speechtotext-331119-820cdd23000d.json"})
    assert speech_text("gs://cloud-samples-data/speech/brooklyn_bridge.raw", True) == "how old is the Brooklyn Bridge"

def test_text_request():
    """Tests a text request sent to the Assistant"""

