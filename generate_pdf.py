import pandas as pd
from fpdf import FPDF, XPos, YPos

class PDF(FPDF):
    def header(self):
        self.set_font('MesloLGS', '', 12)
        self.cell(200, 10, 'Skills Übersicht', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('MesloLGS', '', 10)
        self.cell(0, 10, f'Seite {self.page_no()}', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

# Initialisieren des PDF-Dokuments
pdf = PDF()

# Laden der Schriftarten
pdf.add_font('MesloLGS', '', 'MesloLGS NF.ttf')
pdf.add_font('MesloLGS', 'B', 'MesloLGS NF Bold.ttf')

pdf.add_page()

# Lesen der CSV-Datei
data = pd.read_csv('daten.csv')

# Daten nach Kategorie gruppieren
grouped_data = data.groupby('Kategorie')

# Kategorien und zugehörige Einträge hinzufügen
pdf.set_font('MesloLGS', '', 12)
for category, entries in grouped_data:
    pdf.set_font('MesloLGS', 'B', 12)
    pdf.cell(200, 10, category, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.set_font('MesloLGS', '', 12)
    for index, row in entries.iterrows():
        line = ', '.join(map(str, row.values[1:]))  # assuming the first column is the category
        pdf.cell(200, 10, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.cell(200, 10, '', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')  # leere Zeile

# PDF speichern
pdf.output("skills.pdf")
