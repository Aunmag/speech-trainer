# Speech Trainer

A simple automated speech trainer.

Enhance your speech by identifying and eliminating unwanted words such as fillers and swear words. Create a personalized list of unwanted words and run the app in the background while engaging in activities like audio chats, voice messages or online gaming. The app listens to audio input from the microphone, converts speech to text, and checks for the presence of unwanted words. If an unwanted word is detected, a beep sound is played to alert the speaker, encouraging them to improve their speech habits.

### Setup
- Build the app with Python
    ```sh
    python -m venv .venv
    .venv/Scripts/activate # `".venv/Scripts/activate.bat"` on Windows
    python -m pip install -r requirements.txt
    ```
- Download a [speech-to-text VOSK model](https://alphacephei.com/vosk/models) for your language (e.g: `vosk-model-small-ru-0.22`)
- Configure the settings for you needs in `src/settings.py`
    - At least set the `MODEL_PATH` variable to the unzipped directory of VOSK model
    - Adjust the list of unwanted and ignored words
- Run the app
    ```sh
    ".venv/Scripts/python" src/main.py
    ```
