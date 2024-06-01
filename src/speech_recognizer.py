from queue import Queue
from threading import Thread
from typing import Optional, Any
from vosk import KaldiRecognizer, Model
import json
import logging
import sounddevice as sd
import sys


class SpeechRecognizer:
    def __init__(
        self,
        model: Model,
        device: Optional[Any],  # TODO: find type
        sample_rate: Optional[int] = None,
    ):
        self.model = model
        self.device = device

        if sample_rate is None:
            logging.debug("Sample rate not set")
            self.sample_rate = query_device_sample_rate(self.device)
            logging.debug("Sample rate set to %s", self.sample_rate)
        else:
            self.sample_rate = sample_rate

        self.output = Queue()

    def run_blocking(self):
        input = Queue()

        def callback(data, frames, time, status):
            if status:
                print(status, file=sys.stderr)  # TODO: what?

            input.put(bytes(data), block=False)

        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                device=self.device,
                dtype="int16",
                latency="low",
                channels=1,
                callback=callback,
            ):
                logging.debug("Started")
                recognizer = KaldiRecognizer(self.model, self.sample_rate)

                while True:
                    data = input.get()

                    if recognizer.AcceptWaveform(data):
                        # sentence completed
                        sentence = json.loads(recognizer.Result())["text"]

                        if sentence:
                            self.output.put((sentence, True), block=False)
                    else:
                        # sentence updated
                        sentence = json.loads(recognizer.PartialResult())["partial"]

                        if sentence:
                            self.output.put((sentence, False), block=False)

        except KeyboardInterrupt:
            logging.debug("Stopped")
        except Exception as error:
            logging.error("%s", error)
            # TODO: do something

    def run(self) -> Thread:
        thread = Thread(target=self.run_blocking, daemon=True)
        thread.start()
        return thread


def query_device_sample_rate(device) -> int:
    logging.debug("Querying device sample rate")
    return int(sd.query_devices(device, "input")["default_samplerate"])
