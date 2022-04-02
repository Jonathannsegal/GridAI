"""Method for speech-to-text"""
import io
# import click
from google.cloud import speech


def speech_text(input_audio_file, gcs):
    """Convert provided audio file into a text transcript
    if gcs = true use google cloud file, if gcs = false use local file"""

    # Instantiates a client
    client = speech.SpeechClient()

    if gcs:
        audio = speech.RecognitionAudio(uri=input_audio_file)
    else:
        with io.open(input_audio_file, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    return_str = ""

    for result in response.results:
        return_str += result.alternatives[0].transcript
    # print(f"Transcript: {return_str}")
    return return_str
