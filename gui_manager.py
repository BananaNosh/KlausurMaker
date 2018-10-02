from appJar import gui
from extract_vocabs import VocabExtracter
import datetime
import os


def show_information_and_text_window(process_text):
    text_name = "Text"
    number_name = "number"
    name_name = "name"
    date_name = "date"
    directory_name = "directory"
    file_name = "file"

    default_filename = "klausur.docx"

    def press():
        text = app.textArea(text_name)
        if len(text) == 0:
            app.setTextArea(text_name, "Bitte etwas einfügen!")
            return
        number = app.entry(number_name)
        name = app.entry(name_name)
        date = app.entry(date_name)
        title = f"{number}. {name} {date}"
        directory = app.entry(directory_name)
        directory = directory if os.path.isdir(directory) else "."
        filename = app.entry(file_name)
        filename = filename if len(filename) > 0 else default_filename
        name_without_ext, _ = os.path.splitext(filename)
        ext = ".docx"
        app.stop()
        process_text(text, title, os.path.join(directory, name_without_ext + ext))

    with gui("KlausurMaker", "800x400", font={'size':18}) as app:
        app.addEntry(number_name, row=0, column=0)
        app.setEntry(number_name, "1")
        app.addEntry(name_name, row=0, column=1)
        app.setEntry(name_name, "Lateinklausur E1")
        app.addEntry(date_name, row=0, column=2)
        app.setEntry(date_name, (datetime.date.today() + datetime.timedelta(1)).strftime("%d.%m.%y"))
        app.addLabel("header", "Bitte lateinischen Text einfügen:", row=1, colspan=3)
        app.addTextArea(text_name, row=2, colspan=3)
        app.setTextAreaFocus(text_name)
        app.addDirectoryEntry(directory_name, row=3, column=0, colspan=2)
        app.addEntry(file_name, row=3, column=2)
        app.setEntryDefault(file_name, default_filename)
        app.addButtons(["Submit", "Cancel"], [press, app.stop], row=4, column=0)


def show_vocabs(vocabs, process_vocabs):
    frames_name = "TabbedFrame"

    def press():
        vocabs_to_show = []
        indices_of_shown = []
        for i, sentence in enumerate(vocabs):
            shown_in_sentence = []
            indices_of_shown_in_sentence = []
            for j, vocab in enumerate(sentence):
                word_id = f"{i}_{j}"
                if not app.checkBox(f"check_{word_id}"):
                    continue
                new_lemma = app.entry(f"lemma_{word_id}")
                new_adds = app.entry(f"adds_{word_id}")
                new_translation = app.entry(f"translation_{word_id}")
                shown_in_sentence.append((vocab[0], new_lemma, new_adds, new_translation))
                indices_of_shown_in_sentence.extend(vocab[3] if type(vocab[3]) is list else [vocab[3]])
            vocabs_to_show.append(shown_in_sentence)
            indices_of_shown.append(indices_of_shown_in_sentence)
        app.stop()
        process_vocabs(vocabs_to_show, indices_of_shown)

    longest_sentence_count = max(len(sentence) for sentence in vocabs)
    height = min(170 + 42 * longest_sentence_count, 1000)
    width = 1060

    with gui("KlausurMaker", f"{width}x{height}", font={'size':18}) as app:
        app.setSticky("news")
        app.setLocation("CENTER")
        app.setExpand("column")
        app.label("Gefundene Vokabeln:")
        app.startScrollPane("PANE", disabled="horizontal")
        app.setScrollPaneHeight("PANE", height - 80)
        app.setScrollPaneWidth("PANE", width)
        app.startTabbedFrame(frames_name)
        app.setTabbedFrameTabExpand(frames_name, True)
        for i, sentence in enumerate(vocabs):
            app.startTab(f"Satz {i+1}")
            headers = ["Wort", "Grundform", "Zusatz", "Übersetzung"]
            for j, header in enumerate(headers):
                app.label(f"header_{i}_{j}", header, row=0, column=j+1)
            for j, (word, lemma, adds, _, translation) in enumerate(sentence):
                word_id = f"{i}_{j}"
                row = j + 2
                app.addNamedButton("del", f"btn_{word_id}", press, row=row, column=0)
                app.addNamedCheckBox(word, f"check_{word_id}", row=row, column=1, colspan=1)
                lemma_label = f"lemma_{word_id}"
                app.addEntry(lemma_label, row=row, column=2, colspan=1)
                app.setEntry(lemma_label, lemma, callFunction=False)
                adds_label = f"adds_{word_id}"
                app.addEntry(adds_label, row=row, column=3, colspan=1)
                if adds is not None:
                    app.setEntry(adds_label, adds, callFunction=False)
                translation_label = f"translation_{word_id}"
                app.addEntry(translation_label, row=row, column=4)
                app.setEntry(translation_label, translation)
            app.stopTab()
        app.stopTabbedFrame()
        app.stopScrollPane()
        app.buttons(["Submit", "Cancel"], [press, app.stop])


if __name__ == '__main__':
    def on_press(text, title, filename):
        print(title)
        print(text)
        print(filename)
        with open("./templates/test_text.txt", "r") as f:
            text = f.read()
        vocabs, starts_with_numbers, sentences = VocabExtracter().extract_vocabs(text)
        show_vocabs(vocabs, lambda x, y: x)
        print(sentences)

    show_information_and_text_window(on_press)
