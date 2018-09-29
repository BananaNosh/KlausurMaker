from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.shared import Inches, Pt


def create_klausur_template():
    document = Document()
    normal_style = document.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(14)

    heading = document.add_heading("")
    heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    heading.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    font = heading.add_run("1. Lateinklausur E1, 26.09.18").font
    font.name = "Times New Roman"
    font.size = Pt(18)

    sub_heading = document.add_heading("", level=2)
    sub_heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    sub_heading.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = sub_heading.add_run("Thema der Unterrichtseinheit: Bestimmt was von Cicero")
    run.italic = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    # p = document.add_paragraph('A plain paragraph having some ')
    # p.add_run('bold').bold = True
    # p.add_run(' and some ')
    # p.add_run('italic.').italic = True

    # document.add_heading('Heading, level 1', level=1)
    # document.add_paragraph('Intense quote', style='Intense Quote')

    list_para = document.add_paragraph('Übersetze bitte ...', style='List Number')
    list_para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    list_para.style.font.bold = True

    body = document.add_paragraph("1 Quare secedant improbi, secernant se a bonis; in unum locum congregentur, muro denique secernantur a nobis.  2 Desinant insidari consuli, obsidere curiam cum gladiis, comparare faces ad imflammandam urbem. 3 Denique in fronte uniuscuiusque inscriptum sit, quid de re publica sentiat.")
    body.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    body.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    list_para = document.add_paragraph('Aufgaben zur Interretation:', style='List Number')
    list_para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    document.save('demo.docx')


if __name__ == '__main__':
    create_klausur_template()