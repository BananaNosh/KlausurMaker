from appJar import gui
from extract_vocabs import VocabExtracter


def insert_text_window():
    def press():
        print("Text:", app.textArea("Text"))

    with gui("KlausurMaker", "800x400", font={'size':18}) as app:
        app.label("Bitte lateinischen Text einfügen:")
        app.textArea("Text", label=False, focus=True)
        app.buttons(["Submit", "Cancel"], [press, app.stop])


def show_vocabs(vocabs):
    def press():
        print("Text:", app.textArea("Text"))

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
        frames_name = "TabbedFrame"
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
    vocabs = VocabExtracter().extract_vocabs(text)
    show_vocabs(vocabs)