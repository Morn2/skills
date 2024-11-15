import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def read_data_from_csv(file_path):
    data = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['Kategorie']
            if category not in data:
                data[category] = []
            data[category].append((row['Name'], row['Icon']))
    return data

def create_document(filename, data):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Überschrift hinzufügen und unterstreichen
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, height - 25, "Aaron Feldmann Skill Auflistung")
    c.line(50, height - 27.5, width - 50, height - 27.5)  # Unterstrich hinzufügen

    y_position = height - 50
    column_x_positions = [50, width / 2]
    column_index = 0

    left_categories = ["Hardware Kentnisse", "Arbeitsabläufe", "Hardware Reparatur", "Erklärung"]

    for category, items in data.items():
        if category in left_categories:
            column_index = 0
        else:
            column_index = 1

        c.setFont("Helvetica-Bold", 11)
        c.drawString(column_x_positions[column_index], y_position, category)
        y_position -= 10  # Reduziere den Leerraum hier

        for name, icon_path in items:
            if y_position < 40:
                c.showPage()
                y_position = height - 50
                c.setFont("Helvetica-Bold", 11)
                c.drawString(column_x_positions[column_index], y_position, category)
                y_position -= 10

            c.setFont("Helvetica", 11)
            c.drawString(column_x_positions[column_index], y_position, name)
            y_position -= 10

    c.save()

# Daten aus CSV-Datei lesen
data = read_data_from_csv('daten.csv')

# PDF-Dokument erstellen
create_document("skills.pdf", data)

