from pathlib import Path
import os


ROOT_PATH = Path(__file__).parent.parent
MODEL_PATH = os.path.join(ROOT_PATH, "models/vosk-model-small-ru-0.22")
SOUND_ALERT_PATH = os.path.join(ROOT_PATH, "sounds/alert.wav")
SOUND_STARTUP_PATH = os.path.join(ROOT_PATH, "sounds/startup.wav")
STATISTICS_PATH = os.path.join(ROOT_PATH, "data/statistics.csv")

WORDS_UNWANTED = [
    # fillers
    "вот", "как бы", "короче", "м", "ну", "так", "там", "типа", "то есть", "э",
    # swearing
    "бля", "ебать", "нахуя", "охуеть", "пизда", "пиздец", "сука", "хуй",
]

WORDS_IGNORED = [
    "c", "а", "бы", "в", "же", "за", "и", "из", "к", "ли", "на", "не", "ни",
    "но", "о", "от", "по", "то", "у", "ю", "п",
]
