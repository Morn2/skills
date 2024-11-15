import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

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

    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, height - 25, "Aaron Feldmann Skill Auflistung")
    c.line(50, height - 27.5, width - 50, height - 27.5)

    y_position = height - 50
    column_x_positions = [50, width / 2]

    left_categories = ["Hardware Kentnisse", "Arbeitsabläufe", "Hardware Reparatur"]
    right_categories = ["Software Systeme", "Programierschsprachen", "Software Kentnisse", "Hardware Kentnisse"]

    def draw_text_and_image(c, text, image_path, x, y, font_size):
        c.setFont("Helvetica", font_size)
        text_width = c.stringWidth(text, "Helvetica", font_size)
        c.drawString(x, y, text)
        if image_path and os.path.exists(image_path):
            try:
                image = ImageReader(image_path)
                c.drawImage(image, x + text_width + 5, y - font_size * 0.75, width=font_size, height=font_size)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

    for category in left_categories:
        if category in data:
            c.setFont("Helvetica-Bold", 13)
            c.drawString(column_x_positions[0], y_position, category)
            y_position -= 13

            for name, icon_path in data[category]:
                if y_position < 40:
                    break

                draw_text_and_image(c, name, f"Icons/{icon_path}", column_x_positions[0], y_position, 13)
                y_position -= 13

            y_position -= 20

    y_position = height - 50
    for category in right_categories:
        if category in data:
            c.setFont("Helvetica-Bold", 13)
            c.drawString(column_x_positions[1], y_position, category)
            y_position -= 13

            for name, icon_path in data[category]:
                if y_position < 40:
                    break

                draw_text_and_image(c, name, f"Icons/{icon_path}", column_x_positions[1], y_position, 13)
                y_position -= 13

            y_position -= 20

    if "Erklärung" in data:
        y_position = 100
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Erklärung")
        y_position -= 20

        for name, icon_path in data["Erklärung"]:
            c.setFont("Helvetica", 14)
            c.drawString(50, y_position, name)
            y_position -= 15

    c.save()

# Pfad des aktuellen Skripts ermitteln
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'daten.csv')

# Daten aus CSV-Datei lesen
data = read_data_from_csv(csv_file_path)

# PDF-Dokument erstellen
create_document("skills.pdf", data)
