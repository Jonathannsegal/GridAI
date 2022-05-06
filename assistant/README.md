### Overview 
This Assistant service is used to accept user queries (after natural language processing (NLP)) and handle them accordingly.

---
### Running
Regrettably, the Assistant can not yet be run locally in a straightforward way as there are
issues with python import paths. This may be an easy fix, but we did not dive into it.

However, when launched using the Dockerfile, this service will be hosted successfully.

Furthermore, the Actions on Google service should be enabled. While all code files are
independent of Actions on Google, this Assistant service, so far, should only be used as a
webhook for Actions on Google.

---
### Usage

This Assistant, currently, is intended to only be used as a webhook handler for the Actions on Google service. Using Actions on Google, any Google Assistant interface, such as the Google Assistant app on mobile, can interact with this Assistant. A frontend interface can also be constructed by following one of many React tutorials found with a quick Google search.

This **[Conversational Actions](https://developers.google.com/assistant/conversational/overview)** guides provide the best explanation for how to set up an Actions on Google project, how to define custom actions, how to create a state machine chatbot using [scenes](https://developers.google.com/assistant/conversational/scenes), what request formats to expect, and what response prompts can be returned.

Requests come into the Assistant webhook in a JSON format described [here](https://developers.google.com/assistant/conversational/webhooks#example-request). Similarly, the format for JSON responses from the Assistant are described [here](https://developers.google.com/assistant/conversational/webhooks#example-response).

Currently, this Assistant returns prompts in the [table cards](https://developers.google.com/assistant/conversational/prompts-rich#json_5) and [simple response](https://developers.google.com/assistant/conversational/prompts-simple#json_1) formats.

##### Some important notes
- When creating new releases of your project on Actions on Google, there is a place where you need to make sure to update the "invocation phrases" for your project: ex. "Ok Google, Talk to Grid AI."
	- Deploy -> Directory information -> Additional invocation phrases
	- The name used after "Talk to" must match the name described in Develop -> Settings -> Display name
- When creating new releases of your project on Actions on Google, you cannot use Invocation phrases that are already defined. This leads to one of two outcomes:
	- Deleting an old release and publishing a new one or updating the old release.
		- *However*, our team has not found a way to do this yet.
	- Change the project's display name, update the Invocation phrases, and create a new release.
		- This approach is tedious and inconvenient, but it is the only solution our team found.

---
### Deprecation
Currently, there exist many deprecated features resulting from building in-house
natural language processing (NLP) of user queries. These features include the following:
- assistant_service.py
- create_actions_json.py
- speech_to_text.py
- app.py
	- all functions aside from webhook()
- command_handler.py ()
	- all functions aside from handle_webhook(), generic_query(), and number_of()

Until the frontend has a working Google Assistant integration, retain these deprecated features.

When removing these deprecated features, remember to remove the create_actions_json.py calls from the assistant/Dockerfile and .gitlab-ci.yml files.

---
### Endpoints
- Webhook: Processes request JSON from google assistant
	- Input: Request JSON (See sample JSON)
- ping: responds with "pong" to verify server integrity
- Text (deprecated): Processes text query
	- Input: JSON with the text field set to the query
- Voice (deprecated): Processes voice query
	- Input: JSON with voice field set to the audio file (See accepted audio format).
- setCred (deprecated): Sets google speech-to-text credentials for debug purposes

---
### Audio file format (deprecated)
- A sampling rate of 16 kHz
- 16-bit encoding
- mono audio
- wav, mp3, flac, or raw formats

---
### Sample Google Assistant Request JSON

{
  "requestJson": {
    "handler": {
      "name": "generic_query"
    },
    "intent": {
      "name": "Query_Generic",
      "params": {
        "feature": {
          "original": "voltages",
          "resolved": "VOLTAGE"
        },
        "count": {
          "original": "10",
          "resolved": 10
        },
        "extrema": {
          "original": "top",
          "resolved": "MAX"
        }
      },
      "query": "What are the top 10 voltages"
    },
    "scene": {
      "name": "mainScene",
      "slotFillingStatus": "UNSPECIFIED",
      "slots": {},
      "next": {
        "name": "mainScene"
      }
    },
    "session": {
      "id": "ABwppHE91LJz808wg7DctQ2SnO1ktTmq4GIsQ8z7QottC1evFuTf0ExJxXFsw-zKyt97sbtUghHQmj-V",
      "params": {},
      "typeOverrides": [],
      "languageCode": ""
    },
    "user": {
      "locale": "en-US",
      "params": {},
      "accountLinkingStatus": "ACCOUNT_LINKING_STATUS_UNSPECIFIED",
      "verificationStatus": "VERIFIED",
      "packageEntitlements": [],
      "gaiamint": "",
      "permissions": [],
      "lastSeenTime": "2022-05-02T16:45:45Z"
    },
    "home": {
      "params": {}
    },
    "device": {
      "capabilities": [
        "SPEECH",
        "RICH_RESPONSE",
        "LONG_FORM_AUDIO"
      ],
      "timeZone": {
        "id": "America/Chicago",
        "version": ""
      }
    }
  }
}

# CLient secret

To use speech-to-text.py you must activate the speech-to-text api and add the authentication file here
then uncomment the lines under google authenticcation in the dockerfile.

See https://cloud.google.com/docs/authentication/getting-started for more info.