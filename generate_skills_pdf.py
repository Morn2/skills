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
    c.setFont("Helvetica-Bold", 15)  # Verringert um 1
    c.drawString(50, height - 25, "Aaron Feldmann Skill Auflistung")
    c.line(50, height - 27.5, width - 50, height - 27.5)  # Unterstrich hinzufügen

    y_position = height - 50
    column_x_positions = [50, width / 2]
    column_index = 0

    left_categories = ["Hardware Kentnisse", "Arbeitsabläufe", "Hardware Reparatur"]
    right_categories = ["Software Systeme", "Programierschsprachen", "Software Kentnisse", "Hardware Kentnisse"]

    # Zuerst die linken Kategorien
    for category in left_categories:
        if category in data:
            c.setFont("Helvetica-Bold", 13)  # Verringert um 1
            c.drawString(column_x_positions[0], y_position, category)
            y_position -= 13  # Anpassung des Zeilenabstands

            for name, icon_path in data[category]:
                if y_position < 40:
                    break

                c.setFont("Helvetica", 13)  # Verringert um 1
                c.drawString(column_x_positions[0], y_position, name)
                y_position -= 13  # Anpassung des Zeilenabstands

            y_position -= 20  # Leerschlag zwischen Kategorien

    # Dann die rechten Kategorien
    y_position = height - 50  # Reset y_position for the right column
    for category in right_categories:
        if category in data:
            c.setFont("Helvetica-Bold", 13)  # Verringert um 1
            c.drawString(column_x_positions[1], y_position, category)
            y_position -= 13  # Anpassung des Zeilenabstands

            for name, icon_path in data[category]:
                if y_position < 40:
                    break

                c.setFont("Helvetica", 13)  # Verringert um 1
                c.drawString(column_x_positions[1], y_position, name)
                y_position -= 13  # Anpassung des Zeilenabstands

            y_position -= 20  # Leerschlag zwischen Kategorien

    # Erklärung als separaten Block am Ende der ersten Seite hinzufügen
    if "Erklärung" in data:
        y_position = 130  # Platz für Erklärung am Ende der Seite reservieren
        c.setFont("Helvetica-Bold", 14)  # Verringert um 1
        c.drawString(50, y_position, "Erklärung")
        y_position -= 20  # Anpassung des Zeilenabstands

        for name, icon_path in data["Erklärung"]:
            c.setFont("Helvetica", 14)  # Keine Änderung
            c.drawString(50, y_position, name)
            y_position -= 15  # Anpassung des Zeilenabstands

    c.save()

# Daten aus CSV-Datei lesen
data = read_data_from_csv('daten.csv')

# PDF-Dokument erstellen
create_document("skills.pdf", data)
