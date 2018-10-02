import gui_manager
from extract_vocabs import VocabExtracter
from doc_creater import create_klausur_template
from database_manager import DatabaseManager
import re


def process_text(text, title, filename):
    sentence_delimiters = re.split("[.!?:](\W|)", text)[1:-2:2]
    vocabs, starts_with_numbers, sentences = VocabExtracter().extract_vocabs(text)
    if len(sentence_delimiters) != len(sentences)-1:
        sentence_delimiters = [" "] * (len(sentences) - 1)

    manager = DatabaseManager()
    for i, sentence in enumerate(vocabs):
        words = [vocab[0] for vocab in sentence]
        retrieved_lemma_adds = manager.retrieve_lemma_adds_multiple(words)
        for j, (_, lemma, adds) in enumerate(retrieved_lemma_adds):
            if lemma is not None and adds is not None:
                _, _, translation = manager.retrieve_translation(lemma, adds)
                vocab = vocabs[i][j]
                vocabs[i][j] = (vocab[0], lemma, adds, vocab[3], translation if translation is not None else "")

    def save_info_and_create_doc(vocabs_to_show, indices_of_shown):
        print(vocabs_to_show, indices_of_shown)

        for sentence in vocabs_to_show:
            for word, lemma, adds, translation in sentence:
                if word and len(word) > 0:
                    manager.insert_lemma_adds(word, lemma, adds)
                if lemma and adds and len(lemma) > 0:
                    manager.insert_translation(lemma, adds, translation)

        manager.close()
        create_klausur_template(filename, title, sentences, sentence_delimiters, vocabs_to_show, indices_of_shown,
                                starts_with_numbers)

    gui_manager.show_vocabs(vocabs, save_info_and_create_doc)


if __name__ == '__main__':
    gui_manager.show_information_and_text_window(process_text)