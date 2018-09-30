from appJar import gui
from extract_vocabs import VocabExtracter


def insert_text_window(process_text):
    def press():
        text = app.textArea("Text")
        print("Text:", text)
        app.stop()
        process_text(text)

    with gui("KlausurMaker", "800x400", font={'size':18}) as app:
        app.label("Bitte lateinischen Text einfügen:")
        app.textArea("Text", label=False, focus=True)
        app.buttons(["Submit", "Cancel"], [press, app.stop])


def show_vocabs(vocabs, process_vocabs):
    frames_name = "TabbedFrame"

    def press():
        vocabs_to_show = []
        indices_of_shown = []
        for i, sentence in enumerate(vocabs):
            shown_in_sentence = []
            for j, vocab in enumerate(sentence):
                word_id = f"{i}_{j}"
                print(word_id, app.checkBox(f"check_{word_id}"))
                if not app.checkBox(f"check_{word_id}"):
                    continue
                new_lemma = app.entry(f"lemma_{word_id}")
                new_adds = app.entry(f"adds_{word_id}")
                new_translation = app.entry(f"translation_{word_id}")
                shown_in_sentence.append((vocab[0], new_lemma, new_adds, new_translation))
                indices_of_shown.extend(vocab[3] if type(vocab[3]) is list else [vocab[3]])
                print(new_lemma, new_adds, new_translation)
            vocabs_to_show.append(shown_in_sentence)
        print(vocabs_to_show)
        print(indices_of_shown)
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
            for j, (word, lemma, adds, _) in enumerate(sentence):
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
                app.addEntry(f"translation_{word_id}", row=row, column=4)
            app.stopTab()
        app.stopTabbedFrame()
        app.stopScrollPane()
        app.buttons(["Submit", "Cancel"], [press, app.stop])


if __name__ == '__main__':
    # insert_text_window()
    with open("./test_text.txt", "r") as f:
        text = f.read()
    vocabs, starts_with_numbers = VocabExtracter().extract_vocabs(text)
    show_vocabs(vocabs, lambda x: x)