from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image
import csv
import os


def set_icon_parameters(height=13, width=13, y_offset=0):
    return {"height": height, "width": width, "y_offset": y_offset}


def get_color_for_value(value_name):
    colors = {
        "Grundkentnisse": HexColor("#FF9999"),
        "Gutes theoretisches Wissen": HexColor("#FFCC99"),
        "Erfahrung in Praktik und Theorie": HexColor("#FFFF99"),
        "Gute praktische und theoretische Kentnisse": HexColor("#CCFF99"),
        "Sehr gute praktische und theoretische Kentnisse": HexColor("#99CC99"),
    }
    return colors.get(value_name, HexColor("#FFFFFF"))


def colorize_icon(icon_path, output_path, color_hex):
    with Image.open(icon_path) as img:
        img = img.convert("RGBA")
        r, g, b = Image.new("RGB", (1, 1), color_hex).getpixel((0, 0))
        new_data = [
            (r, g, b, item[3]) if item[3] > 0 else item
            for item in img.getdata()
        ]
        img.putdata(new_data)
        img.save(output_path)


def read_data_from_csv(file_path):
    data = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['Kategorie']
            icon = row['Icon'].strip() if row['Icon'] else None
            if category not in data:
                data[category] = []
            data[category].append({
                "Name": row['Name'],
                "Icon": icon,
                "Value": row['Name'] if category == "Erklärung" else None
            })
    return data


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

    icon_params = set_icon_parameters(height=13, width=13, y_offset=7)

    for category, items in data.items():
        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y_position, category)
        y_position -= 20

        for item in items:
            name = item["Name"]
            icon_path = os.path.join(
                icons_folder, item["Icon"]) if item["Icon"] else None
            color = get_color_for_value(item["Value"])
            color_hex = "#{:02x}{:02x}{:02x}".format(
                int(color.red * 255), int(color.green * 255), int(color.blue * 255)
            )

            # Debugging-Ausgabe für Farben
            print(f"Zeile: {name}, Wert: {item['Value']}, Farbe: {color}")

            c.setFillColor(color)
            c.rect(margin, y_position - 13, width -
                   margin, 13, stroke=0, fill=1)
            c.setFillColor(HexColor("#000000"))
            c.setFont("Helvetica", 12)
            c.drawString(margin + 5, y_position - 10, name)

            if icon_path and os.path.isfile(icon_path):
                colored_icon_path = os.path.join(icons_folder, f"colored_{
                                                 os.path.basename(icon_path)}")
                colorize_icon(icon_path, colored_icon_path, color_hex)

                x_position = width - 100
                try:
                    c.drawImage(colored_icon_path, x_position,
                                y_position - icon_params["height"],
                                width=icon_params["width"],
                                height=icon_params["height"], mask='auto')
                except Exception as e:
                    print(f"Fehler bei Icon '{icon_path}': {e}")

            y_position -= 20
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

