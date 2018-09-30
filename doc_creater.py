from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor


def create_klausur_template(filename, title, text, vocabs_to_show, indices_of_shown, show_numbers=False):
    document = Document()
    normal_style = document.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(14)

    heading = document.add_heading("")
    heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    heading.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    font = heading.add_run(title).font
    font.name = "Times New Roman"
    font.size = Pt(18)
    font.color.rgb = RGBColor(0,0,0)

    sub_heading = document.add_heading("", level=2)
    sub_heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    sub_heading.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = sub_heading.add_run("Thema der Unterrichtseinheit: Bestimmt was von Cicero")
    run.italic = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0,0,0)

    # p = document.add_paragraph('A plain paragraph having some ')
    # p.add_run('bold').bold = True
    # p.add_run(' and some ')
    # p.add_run('italic.').italic = True

    # document.add_heading('Heading, level 1', level=1)
    # document.add_paragraph('Intense quote', style='Intense Quote')

    list_para = document.add_paragraph('Übersetze bitte ...', style='List Number')
    list_para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    list_para.style.font.bold = True

    body = document.add_paragraph(text)
    body.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    body.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    help_style = document.styles.add_style("Vocab Help", WD_STYLE_TYPE.PARAGRAPH)
    help_style.base_style = document.styles["Normal"]
    help_style.font.size = Pt(9)
    help_style.font.bold = True
    vocab_help_para = document.add_paragraph("", style="Vocab Help")
    vocab_help_para.add_run("Übersetzungshilfen:").italic = True
    for i, sentence in enumerate(vocabs_to_show):
        if show_numbers and len(sentence) > 0:
            vocab_help_para.add_run(f" {i+1}")
        for j, (word, lemma, adds, translation) in enumerate(sentence):
            adds_string = f", {adds}" if adds is not None and len(adds) > 0 else ""
            vocab_string = f" {lemma}{adds_string} - {translation}"
            vocab_string = " " + vocab_string.replace(" ", u"\xa0").strip()
            print(vocab_string)
            vocab_help_para.add_run(vocab_string)
            vocab_help_para.add_run("," if j < len(sentence)-1 else ".")

    list_para = document.add_paragraph('Aufgaben zur Interretation:', style='List Number')
    list_para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    document.save(filename)


if __name__ == '__main__':
    filename = "demo.docx"
    title = "1. Lateinklausur E1 26.09.18"
    with open("./test_text.txt", "r") as f:
        test_text = f.read()
    vocabs = [[('Quare', 'quare', '', 'Deshalb'), ('congregentur', 'congregari', '', 'sich zusammenscharen')],
              [('Desinant', 'desinare', '', 'aufhören'),
               ('insidari', 'insidari', 'c. Dat', 'jemandem nach dem Leben trachten'),
               ('faces', 'fax', 'facis f', 'Fackel')], [], [], []]
    create_klausur_template(filename, title, test_text, vocabs, [0, 10, 0, 1, 8], True)
