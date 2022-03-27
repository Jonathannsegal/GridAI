"""Method for speech-to-text"""
# import io
# import click
# from google.cloud import speech


# @click.command()
# @click.option('--gcs-audio', '-i', required=True,
#               metavar='<input file>', type=str,
#               help='Path to input audio file (format: LINEAR16 16000 Hz).')
def speech_text():
    """Convert provided audio file into a text transcript"""

    # Instantiates a client
    # client = speech.SpeechClient()

    # with io.open(input_audio_file, "rb") as audio_file:
    #     content = audio_file.read()

    # audio = speech.RecognitionAudio(uri=gcs_audio)
    # audio = speech.RecognitionAudio(content=content)
    # config = speech.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     sample_rate_hertz=16000,
    #     language_code="en-US",
    # )

    # Detects speech in the audio file
    # response = client.recognize(config=config, audio=audio)

    # return_str = ""

    # for result in response.results:
    #     return_str += result.alternatives[0].transcript
    # print(f"Transcript: {return_str}")
    return "how old is the Brooklyn Bridge"


# if __name__ == '__main__':
#     speech_text()  # pylint: disable=no-value-for-parameter
