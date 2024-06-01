import logging
from typing import List


class Analyzer:
    def __init__(self, unwanted_words: List[str]):
        self.sentence = []
        self.unwanted_words = unwanted_words

    def update_sentence(self, sentence_raw, on_trigger):
        sentence_for_logging = []
        sentence = sentence_raw.strip().split(" ")
        is_sentence_changed = False

        for i, word in enumerate(sentence):
            is_word_appended = i + 1 > len(self.sentence)
            is_word_changed = not is_word_appended and word != self.sentence[i]
            is_word_unwanted = False

            if is_word_appended or is_word_changed:
                if word in self.unwanted_words:
                    is_word_unwanted = True
                    on_trigger(sentence, i)

                is_sentence_changed = True

            # TODO: do this only if debug is enables:
            word_for_log = word

            if is_word_appended:
                word_for_log = "\x1b[32;1m" + word_for_log
            if is_word_changed:
                word_for_log = "\x1b[33;1m" + word_for_log
            if is_word_unwanted:
                word_for_log = "\x1b[4m" + word_for_log
            if is_word_appended or is_word_changed or is_word_unwanted:
                word_for_log = word_for_log + "\x1b[0m"

            sentence_for_logging.append(word_for_log)

        if is_sentence_changed:
            self.sentence = sentence
            logging.debug("Sentence updated: %s", " ".join(sentence_for_logging))

    def clear(self):
        self.sentence = []
        logging.debug("Sentence completed")
