from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image
import csv
import os


def set_icon_parameters(height=20, width=20, y_offset=0):
    return {"height": height, "width": width, "y_offset": y_offset}

# Funktion zur Farbzuordnung basierend auf numerischen Werten


def get_color_for_value(value):
    if value == "1":
        return HexColor("#ADD8E6")  # Hellblau
    elif value == "2":
        return HexColor("#87CEEB")  # Mittelblau
    elif value == "3":
        return HexColor("#4682B4")  # Dunkelgrün
    elif value == "4":
        return HexColor("#5F9EA0")  # Kräftiges Blaugrün
    elif value == "5":
        return HexColor("#2E8B57")  # Dunkelgrün
    else:
        return HexColor("#FFFFFF")  # Standard: Weiß


# Daten aus CSV lesen


def read_data_from_csv(file_path):
    data = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['Kategorie']
            icon = row['Icon'].strip() if row['Icon'] else None
            value = row['Wert'].strip(
            ) if 'Wert' in row and row['Wert'] else None
            if category not in data:
                data[category] = []
            data[category].append({
                "Name": row['Name'],
                "Icon": icon,
                "Value": value
            })
    return data

# PDF erstellen


def create_pdf(filename, data, icons_folder):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 50
    y_position = height - margin
    column_width = (width - 2 * margin) / 2

    c.setFont("Helvetica-Bold", 15)
    c.drawString(margin, y_position, "Aaron Feldmann Skill Auflistung")
    c.line(margin, y_position - 2.5, width - margin, y_position - 2.5)
    y_position -= 30

    icon_params = set_icon_parameters(height=20, width=20, y_offset=7)

    for category, items in data.items():
        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y_position, category)
        y_position -= 20

        for item in items:
            name = item["Name"]
            icon_path = os.path.join(
                icons_folder, item["Icon"]) if item["Icon"] else None
            color = get_color_for_value(item["Value"])
            num_icons = int(
                item["Value"]) if item["Value"] and item["Value"].isdigit() else 1

            # Hintergrund für Icons
            if icon_path and os.path.isfile(icon_path):
                rect_width = num_icons * (icon_params["width"] + 5) + 10
                rect_height = icon_params["height"] + 10
                c.setFillColor(color)
                c.rect(margin + 100, y_position - rect_height,
                       rect_width, rect_height, stroke=0, fill=1)

                # Icons zeichnen
                try:
                    for i in range(num_icons):
                        x_position = margin + 105 + i * \
                            (icon_params["width"] + 5)
                        c.drawImage(icon_path, x_position, y_position - rect_height + 5,
                                    width=icon_params["width"],
                                    height=icon_params["height"], mask='auto')
                except Exception as e:
                    print(f"Fehler bei Icon '{icon_path}': {e}")

            # Text zeichnen
            c.setFillColor(HexColor("#000000"))  # Textfarbe schwarz
            c.setFont("Helvetica", 12)
            c.drawString(margin + 5, y_position - 10, name)

            y_position -= 30
            if y_position < margin:
                c.showPage()
                y_position = height - margin

    c.save()


script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'daten.csv')
icons_folder = os.path.join(script_dir, 'Icons')
output_pdf_path = os.path.join(script_dir, 'skills_colored_final.pdf')

data = read_data_from_csv(csv_file_path)
create_pdf(output_pdf_path, data, icons_folder)
