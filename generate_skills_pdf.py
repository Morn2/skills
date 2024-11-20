from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import csv
import os
from PIL import Image

# Funktion zur Einstellung der Icon-Parameter


def set_icon_parameters(height=13, width=13, y_offset=0):
    return {"height": height, "width": width, "y_offset": y_offset}

# Debugging-Datei initialisieren


def initialize_debugging_file(debug_file):
    with open(debug_file, 'w') as f:
        f.write("Debugging Log for Missing Icons\n")
        f.write("="*40 + "\n")

# Fehlende Icons protokollieren


def log_missing_icon(debug_file, icon_name, reason):
    with open(debug_file, 'a') as f:
        f.write(f"Missing Icon: {icon_name}, Reason: {reason}\n")

# Text und Bild zeichnen


def draw_text_and_image(c, text, image_path, x, y, font_size, icon_params, debug_file):
    c.setFont("Helvetica", font_size)
    text_width = c.stringWidth(text, "Helvetica", font_size)
    c.drawString(x, y, text)
    # Get the absolute path of the icon
    file_info = os.path.abspath(image_path)
    with open(debug_file, 'a') as f:
        f.write(f"Processing text: '{text}' with icon: '{
                image_path}' at position: ({x}, {y}), File Info: {file_info}\n")
    if image_path and os.path.exists(image_path):
        try:
            image = Image.open(image_path)
            temp_image_path = "temp_image.png"
            image.save(temp_image_path)  # Temporär als PNG speichern
            image_reader = ImageReader(temp_image_path)
            c.drawImage(image_reader, x + text_width + 5, y - font_size * 0.75 + icon_params["y_offset"],
                        width=icon_params["width"], height=icon_params["height"])
            with open(debug_file, 'a') as f:
                f.write(f"Successfully loaded icon: '{
                        image_path}', File Info: {file_info}\n")
            os.remove(temp_image_path)  # Temporäre Datei entfernen
        except Exception as e:
            log_missing_icon(debug_file, image_path,
                             f"Error loading image: {e}")
    else:
        log_missing_icon(debug_file, image_path, "File does not exist")

# CSV-Daten lesen


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

# PDF-Dokument erstellen


def create_document(filename, data, debug_file):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, height - 25, "Aaron Feldmann Skill Auflistung")
    c.line(50, height - 27.5, width - 50, height - 27.5)

    y_position = height - 50
    column_x_positions = [50, width / 2]

    left_categories = ["Hardware Kentnisse",
                       "Arbeitsabläufe", "Hardware Reparatur"]
    right_categories = ["Software Systeme", "Programierschsprachen",
                        "Software Kentnisse", "Hardware Kentnisse"]

    icon_params = set_icon_parameters(height=13, width=13, y_offset=7)

    for category in left_categories:
        if category in data:
            c.setFont("Helvetica-Bold", 13)
            c.drawString(column_x_positions[0], y_position, category)
            y_position -= 13

            for name, icon_path in data[category]:
                if y_position < 40:
                    break

                draw_text_and_image(
                    c, name, f"Icons/{icon_path}", column_x_positions[0], y_position, 13, icon_params, debug_file)
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

                draw_text_and_image(
                    c, name, f"Icons/{icon_path}", column_x_positions[1], y_position, 13, icon_params, debug_file)
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

    # Save the canvas and log the save action
    c.save()
    with open(debug_file, 'a') as f:
        f.write(f"PDF saved as: {filename}\n")


# Pfad des aktuellen Skripts ermitteln
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'daten.csv')
debug_file_path = os.path.join(script_dir, 'debug_log.txt')

# Debugging-Datei initialisieren
initialize_debugging_file(debug_file_path)

# Daten aus CSV-Datei lesen
data = read_data_from_csv(csv_file_path)

# PDF-Dokument erstellen
create_document("skills.pdf", data, debug_file_path)
