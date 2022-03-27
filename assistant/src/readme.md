# Run Localy

-Set up virtual envirment

Download Dependencies
sudo apt-get install portaudio19-dev libffi-dev libssl-dev
python -m pip install --upgrade google-assistant-sdk

Install authorization tool
python -m pip install --upgrade google-auth-oauthlib[tool]

-Generate credentials and go to outputed url to get authorization code to enter
google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save --headless --client-secrets ./assistant/client_secret/client_secret_672972911364-gdaunu2a47t0hmfbn11ec1rsumr1i05c.apps.googleusercontent.com.json

device instance id: ac47efee-98bf-11ec-a59e-9cb6d0fe6b0a

-Run
-audio file input
python ./assistant/src/audioFileInput.py --device-model-id speechtotext-331119-gridaitest-tuoi4c --device-id ac47efee-98bf-11ec-a59e-9cb6d0fe6b0a -o output.wav -i Path/To/Input

-Text input
python ./assistant/src/textinput.py --device-model-id speechtotext-331119-gridaitest-tuoi4c --device-id ac47efee-98bf-11ec-a59e-9cb6d0fe6b0a
