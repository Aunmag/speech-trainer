from typing import List
import csv
import logging
import schedule


class Statistics:
    def __init__(self, path: str, ignored_words: List[str]):
        self.path = path
        self.words = {}
        self.ignored_words = ignored_words
        self.auto_save = False
        self.is_updated = False

    def add_word(self, word: str):
        word = normalize_word(word)

        if word is not None and word not in self.ignored_words:
            if word in self.words:
                self.words[word] = self.words[word] + 1
            else:
                self.words[word] = 1

            self.is_updated = True

    def add_sentence(self, sentence: List[str]):
        for word in sentence:
            self.add_word(word)

    def load(self):
        logging.info("Loading from %s", self.path)

        try:
            for line in csv.read(self.path, True):
                self.words[line.get_as_str(0)] = line.get_as_int(1)

            logging.info("Loaded")
        except FileNotFoundError:
            logging.warn("Not found. New statistics will be started")

        self.is_updated = False

    def save(self):
        if not self.is_updated:
            return

        logging.info("Saving to %s", self.path)

        try:
            with open(self.path, "w+", encoding="UTF-8") as file:
                for word, n in sorted(self.words.items(), key=lambda i: i[1], reverse=True):
                    file.write(word)
                    file.write(";")
                    file.write(str(n))
                    file.write("\n")

            self.is_updated = False
        except IOError as error:
            logging.error("Failed to save: %s", error)
        else:
            logging.info("Saved")  # TODO: measure time

    def run_auto_save_task(self):
        if self.auto_save:
            return

        self.auto_save = True
        schedule.every(1).minutes.do(lambda: self.save)
        logging.info("Auto save enabled")


def normalize_word(word: str) -> str:
    if word is not None:
        word = word.lower()

        if word == "" or word == " ":
            word = None

    return word
