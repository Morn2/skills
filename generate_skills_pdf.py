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
            data[category].append((row['Name'], row['Icon'], int(row['Wert'])))
    return data

def create_document(filename, data):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Überschrift hinzufügen und unterstreichen
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Aaron Feldmann Skill Auflistung")
    c.line(100, height - 55, width - 100, height - 55)  # Unterstrich hinzufügen

    y_position = height - 100

    for category, items in data.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, category)
        y_position -= 20

        for name, icon_path, value in items:
            c.setFont("Helvetica", 12)
            c.drawString(100, y_position, f"{name} ({value})")
            y_position -= 20

        y_position -= 20  # Leerschlag zwischen Kategorien

    c.save()

# Daten aus CSV-Datei lesen
data = read_data_from_csv('daten.csv')

# PDF-Dokument erstellen
create_document("skills.pdf", data)


