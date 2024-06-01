from analyzer import Analyzer
from playsound import playsound
from speech_recognizer import SpeechRecognizer
from statistics import Statistics
from threading import Thread
import logging
import schedule
import settings
import sys
import time
import vosk


def main():
    init_logger()
    init_scheduler()

    model = vosk.Model(settings.MODEL_PATH)

    recognizer = SpeechRecognizer(model, None, sample_rate=16_000)
    recognizer_output = recognizer.output
    recognizer.run()

    statistics = Statistics(settings.STATISTICS_PATH, settings.WORDS_IGNORED)
    statistics.load()
    statistics.run_auto_save_task()

    analyzer = Analyzer(settings.WORDS_UNWANTED)  # TODO: merge with recognizer

    playsound(settings.SOUND_STARTUP_PATH)

    while True:
        try:
            sentence, is_complete = recognizer_output.get()
            analyzer.update_sentence(sentence, on_trigger)

            if is_complete:
                statistics.add_sentence(analyzer.sentence)
                analyzer.clear()
        except KeyboardInterrupt:
            break

    statistics.save()
    logging.info("Stopped")


def init_logger():
    logging.basicConfig(
        level=logging.DEBUG,  # TODO: make configurable
        stream=sys.stdout,
        format="%(asctime)s %(levelname)-8s [%(filename)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def init_scheduler():
    def task():
        while True:
            time.sleep(1)
            schedule.run_pending()

    thread = Thread(target=task, daemon=True)
    thread.start()


def on_trigger(sentence, word_index):
    playsound(settings.SOUND_ALERT_PATH)


if __name__ == "__main__":
    main()
