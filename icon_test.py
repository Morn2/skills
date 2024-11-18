from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import csv
import os

# Funktion zur Einstellung der Icon-Parameter
def set_icon_parameters(height=50, width=50, y_offset=0):
    return {"height": height, "width": width, "y_offset": y_offset}

# Debugging-Datei initialisieren
def initialize_debugging_file(debug_file):
    with open(debug_file, 'w') as f:
        f.write("Debugging Log for Icon Test\n")
        f.write("="*40 + "\n")

# Fehlende Icons protokollieren
def log_missing_icon(debug_file, icon_name, reason, file_info):
    with open(debug_file, 'a') as f:
        f.write(f"Missing Icon: {icon_name}, Reason: {reason}, File Info: {file_info}\n")

# Funktion zum Zeichnen von Text und Bild
def draw_text_and_image(c, text, image_path, x, y, font_size, icon_params, debug_file):
    c.setFont("Helvetica", font_size)
    text_width = c.stringWidth(text, "Helvetica", font_size)
    c.drawString(x, y, text)
    file_info = os.path.abspath(image_path)  # Get the absolute path of the icon
    with open(debug_file, 'a') as f:
        f.write(f"Processing text: '{text}' with icon: '{image_path}' at position: ({x}, {y}), File Info: {file_info}\n")
    if image_path and os.path.exists(image_path):
        try:
            image = ImageReader(image_path)
            c.drawImage(image, x + text_width + 5, y - font_size * 0.75 + icon_params["y_offset"],
                        width=icon_params["width"], height=icon_params["height"])
            with open(debug_file, 'a') as f:
                f.write(f"Successfully loaded icon: '{image_path}', File Info: {file_info}\n")
        except Exception as e:
            log_missing_icon(debug_file, image_path, f"Error loading image: {e}", file_info)
    else:
        log_missing_icon(debug_file, image_path, "File does not exist", file_info)

# CSV-Daten lesen
def read_data_from_csv(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((row['Name'], row['Icon']))
    return data

# PDF-Dokument erstellen
def create_document(filename, data, debug_file):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, height - 25, "Icon Test PDF")
    c.line(50, height - 27.5, width - 50, height - 27.5)

    y_position = height - 50
    icon_params = set_icon_parameters(height=50, width=50, y_offset=0)

    for name, icon_path in data:
        if y_position < 60:
            c.showPage()
            y_position = height - 50

        draw_text_and_image(c, name, f"Icons/{icon_path}", 50, y_position, 13, icon_params, debug_file)
        y_position -= 60

    c.save()

# Pfad des aktuellen Skripts ermitteln
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'daten.csv')
debug_file_path = os.path.join(script_dir, 'icon_test_debug_log.txt')

# Debugging-Datei initialisieren
initialize_debugging_file(debug_file_path)

# Daten aus CSV-Datei lesen
data = read_data_from_csv(csv_file_path)

# PDF-Dokument erstellen
create_document("icon_test.pdf", data, debug_file_path)
