import os
import csv
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def set_icon_parameters(height=20, width=20, y_offset=0):
    return {"height": height, "width": width, "y_offset": y_offset}


def get_color_for_value(value):
    if value == "1":
        return HexColor("#ADD8E6")  # Hellblau
    elif value == "2":
        return HexColor("#87CEEB")  # Mittelblau
    elif value == "3":
        return HexColor("#4682B4")  # Dunkelgrün
    elif value == "4":
        return HexColor("#5F9EA0")  # Blaugrün
    elif value == "5":
        return HexColor("#2E8B57")  # Dunkelgrün
    else:
        return HexColor("#FFFFFF")  # Standard: Weiß


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


def create_pdf(filename, data, icons_folder):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 50
    bottom_margin = 100
    y_position_left = height - margin - 35
    y_position_right = height - margin - 35
    column_width = (width - 2 * margin) / 2

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, height - -10 - margin,
                 "Aaron Feldmann Skill Auflistung")
    c.line(margin, height - margin - 10, width - margin, height - margin - 10)

    y_position_left -= -30
    y_position_right -= -30

    icon_params = set_icon_parameters(height=13, width=13, y_offset=3)

    left_categories = ["Hardware Kentnisse",
                       "Arbeitsabläufe", "Hardware Reparatur"]
    right_categories = ["Software Systeme",
                        "Programiersprachen", "Software Kentnisse"]

    for category, items in data.items():
        if category in left_categories:
            y_position = y_position_left
            x_position = margin
        elif category in right_categories:
            y_position = y_position_right
            x_position = margin + column_width
        else:
            continue

        y_position -= 10
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(HexColor("#000000"))
        c.drawString(x_position, y_position, category)
        y_position -= 5

        for item in items:
            name = item["Name"]
            icon_path = os.path.join(
                icons_folder, item["Icon"]) if item["Icon"] else None
            color = get_color_for_value(item["Value"])
            num_icons = int(
                item["Value"]) if item["Value"] and item["Value"].isdigit() else 1

            c.setFillColor(HexColor("#000000"))
            c.setFont("Helvetica", 10)
            c.drawString(x_position + 5, y_position - 10, name)

            text_width = c.stringWidth(name, "Helvetica", 10)

            if icon_path and os.path.isfile(icon_path):
                try:
                    for i in range(num_icons):
                        icon_x_position = x_position + 15 + text_width + i * (
                            icon_params["width"] + 5
                        )
                        c.setFillColor(color)
                        c.rect(
                            icon_x_position - 5,
                            y_position - 15,
                            icon_params["width"] + 10,
                            icon_params["height"],
                            stroke=0,
                            fill=1,
                        )
                        c.drawImage(
                            icon_path,
                            icon_x_position,
                            y_position - 15,
                            width=icon_params["width"],
                            height=icon_params["height"],
                            mask="auto",
                        )
                except Exception as e:
                    print(f"Fehler bei Icon '{icon_path}': {e}")

            y_position -= 20

        if category in left_categories:
            y_position_left = y_position
        elif category in right_categories:
            y_position_right = y_position

    explanation_x = margin + column_width
    explanation_y = 300

    c.setFont("Helvetica-Bold", 12)
    c.drawString(explanation_x, explanation_y + 20, "Erklärung")

    c.setFont("Helvetica", 10)
    for item in data.get("Erklärung", []):
        name = item["Name"]
        color = get_color_for_value(item["Value"])
        c.setFillColor(color)
        c.rect(explanation_x, explanation_y, 225, 15, stroke=0, fill=1)
        c.setFillColor(HexColor("#000000"))
        c.drawString(explanation_x + 5, explanation_y + 3, name)
        explanation_y -= 20

    c.save()


script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "daten.csv")
icons_folder = os.path.join(script_dir, "Icons")
output_pdf_path = os.path.join(script_dir, "skills_colored_final.pdf")

data = read_data_from_csv(csv_file_path)
create_pdf(output_pdf_path, data, icons_folder)
