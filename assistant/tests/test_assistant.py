# pylint: disable=line-too-long
# import os
# from assistant.src.app import *
# from assistant.src.speech_to_text import *
# from assistant.src.app import app
# import pytest


# @pytest.fixture
# def client():
#     """Pytest client fixture"""
#     with app.test_client() as client:
#         yield client

# def test_webhook(client):
#     """Tests webhook"""
#     requestJson = {
#         "handler": {
#             "name": "generic_query"
#         },
#         "intent": {
#             "name": "Query_Generic",
#             "params": {
#             "feature": {
#                 "original": "voltages",
#                 "resolved": "VOLTAGE"
#             },
#             "count": {
#                 "original": "10",
#                 "resolved": 10
#             },
#             "time_comparator": {
#                 "original": "",
#                 "resolved": [
#                     "BEFORE",
#                     "AFTER"
#                 ]
#             },
#             "times": {
#                 "original": "",
#                 "resolved": [
#                 {
#                     "year": 2022,
#                     "day": 27,
#                     "month": 4
#                 },
#                 {
#                     "day": 20,
#                     "year": 2022,
#                     "month": 4
#                 }
#                 ]
#             },
#             "range_values": {
#                 "original": "",
#                 "resolved": [
#                 "between 2 and 3"
#                 ]
#             },
#             "extrema": {
#                 "original": "top",
#                 "resolved": "MAX"
#             }
#             },
#"query": "Get the top 10 voltages between 2 and 3 volts before tomorrow and after yesterday"
#         },
#         "scene": {
#             "name": "mainScene",
#             "slotFillingStatus": "UNSPECIFIED",
#             "slots": {},
#             "next": {
#             "name": "mainScene"
#             }
#         },
#         "session": {
#"id": "ABwppHFF8iGrW6HwSO10It2dVJIYI7ymYcbEKeJfcqTJfdtLeHkmXD3BvKlo5cY_mq5GJwKexLvBj-uc",
#             "params": {},
#             "typeOverrides": [],
#             "languageCode": ""
#         },
#         "user": {
#             "locale": "en-US",
#             "params": {},
#             "accountLinkingStatus": "ACCOUNT_LINKING_STATUS_UNSPECIFIED",
#             "verificationStatus": "VERIFIED",
#             "packageEntitlements": [],
#             "gaiamint": "",
#             "permissions": [],
#             "lastSeenTime": "2022-04-25T17:16:25Z"
#         },
#         "home": {
#             "params": {}
#         },
#         "device": {
#             "capabilities": [
#             "SPEECH",
#             "RICH_RESPONSE",
#             "LONG_FORM_AUDIO"
#             ],
#             "timeZone": {
#             "id": "America/Chicago",
#             "version": ""
#             }
#         }
#     }
#     res = client.post(
#         '/webhook',
#         json=requestJson
#     )
#     assert res.status_code == 200

# def test_speech():
#     """speech to text test"""
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
#         os.getcwd() + "/assistant/client_secret/speechtotext-331119-820cdd23000d.json"
#     assert speech_text("gs://cloud-samples-data/speech/brooklyn_bridge.raw", True) \
#          == "how old is the Brooklyn Bridge"
#     assert speech_text(os.getcwd() + "/assistant/test_voice_files/house/0a7c2a8d_nohash_0.wav",
#                        False) == "house"

# def test_text_request(client):
#     """Tests a text request sent to the Assistant"""
#     ret = client.post(
#         '/text',
#         json={
#             "text": "Show voltages less than 100",
#         }
#     )
#     assert ret.status_code == 200

# def test_app_speech():
#     """Test voice_to_text in app"""
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
#         os.getcwd() + "/assistant/client_secret/speechtotext-331119-820cdd23000d.json"
#     assert voice_to_text(os.getcwd() + "/assistant/test_voice_files/house/0a7c2a8d_nohash_0.wav")\
#          == "house"

# def test_allowed_file():
#     """Test allowed extensions"""
#     assert allowed_file("abc.wav")
#     assert not allowed_file("abc.png")
