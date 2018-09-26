from appJar import gui


def insert_text_window():
    def press():
        print("Text:", app.textArea("Text"))

    with gui("KlausurMaker", "800x400", font={'size':18}) as app:
        app.label("Bitte lateinischen Text einfügen:")
        app.textArea("Text", label=False, focus=True)
        app.buttons(["Submit", "Cancel"], [press, app.stop])


def show_vocabs():
    def press():
        print("Text:", app.textArea("Text"))

    vocabs = []
    with gui("KlausurMaker", "800x400", font={'size':18}) as app:
        app.label("Gefundene Vokabeln:")

        app.buttons(["Submit", "Cancel"], [press, app.stop])


if __name__ == '__main__':
    # insert_text_window()
show_vocabs()