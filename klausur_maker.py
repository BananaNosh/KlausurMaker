import gui_manager
from extract_vocabs import VocabExtracter
from doc_creater import create_klausur_template


def process_text(text):
    vocabs, starts_with_numbers = VocabExtracter().extract_vocabs(text)

    def create_doc(vocabs_to_show, indices_of_shown):
        title = "1. Lateinklausur E1, 26.09.18"
        filename = "demo.docx"
        print(vocabs_to_show, indices_of_shown)
        create_klausur_template(filename, title, text, vocabs_to_show, indices_of_shown, starts_with_numbers)

    gui_manager.show_vocabs(vocabs, create_doc)


if __name__ == '__main__':
    gui_manager.insert_text_window(process_text)