import gui_manager
from extract_vocabs import VocabExtracter
from doc_creater import create_klausur_template
import re


def process_text(text, title, filename):
    sentence_delimiters = re.split("[.!?:](\W|)", text)[1:-2:2]
    vocabs, starts_with_numbers, sentences = VocabExtracter().extract_vocabs(text)
    if len(sentence_delimiters) != len(sentences)-1:
        sentence_delimiters = [" "] * (len(sentences) - 1)

    def create_doc(vocabs_to_show, indices_of_shown):
        print(vocabs_to_show, indices_of_shown)
        create_klausur_template(filename, title, sentences, sentence_delimiters, vocabs_to_show, indices_of_shown,
                                starts_with_numbers)

    gui_manager.show_vocabs(vocabs, create_doc)


if __name__ == '__main__':
    gui_manager.show_information_and_text_window(process_text)