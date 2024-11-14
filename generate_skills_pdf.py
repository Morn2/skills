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
    c.setFont("Helvetica-Bold", 8)  # Schriftgröße halbiert
    c.drawString(100, height - 25, "Aaron Feldmann Skill Auflistung")
    c.line(100, height - 27.5, width - 100, height - 27.5)  # Unterstrich hinzufügen

    y_position = height - 50

    for category, items in data.items():
        c.setFont("Helvetica-Bold", 6)  # Schriftgröße halbiert
        c.drawString(100, y_position, category)
        y_position -= 10

        for name, icon_path in items:
            c.setFont("Helvetica", 6)  # Schriftgröße halbiert
            c.drawString(100, y_position, name)
            y_position -= 10

        y_position -= 10  # Leerschlag zwischen Kategorien

    c.save()

# Daten aus CSV-Datei lesen
data = read_data_from_csv('daten.csv')

# PDF-Dokument erstellen
create_document("skills.pdf", data)


