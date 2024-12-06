import os
import csv
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def get_user_name():
    """
    Fragt den Namen des Benutzers ab und gibt ihn zurück.
    """
    return input("Bitte geben Sie Ihren Namen ein: ")


def read_data_from_csv(file_path):
    """
    Liest die Daten aus einer CSV-Datei und gibt sie als Dictionary zurück.
    """
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


def set_icon_parameters(height=13, width=13, y_offset=3):
    """
    Definiert Standardparameter für Icons.
    """
    return {"height": height, "width": width, "y_offset": y_offset}


def get_color_for_value(value):
    """
    Gibt die entsprechende Farbe jeden Wert.
    """
    if value == "1":
        return HexColor("#c68fcf")  # Pastell Rosa
    elif value == "2":
        return HexColor("#b56bff")  # Pastell Flieder
    elif value == "3":
        return HexColor("#90CAF9")  # Pastell Hellblau
    elif value == "4":
        return HexColor("#4DD0E1")  # Pastell Türkis
    elif value == "5":
        return HexColor("#66BB6A")  # Frisches Hellgrün
    else:
        return HexColor("#FFFFFF")  # Standard Weiß (Fallback)


def create_pdf(filename, data, icons_folder, user_name):
    """
    Erstellt ein PDF mit den Daten aus der CSV-Datei, Icons und Benutzername.
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 50
    bottom_margin = 100
    column_width = (width - 2 * margin) / 1.9

    # Überschrift und Linie
    add_header(c, width, height, margin, user_name)

    # Kategorien zeichnen
    draw_categories(c, data, icons_folder, height, width, margin, column_width)

    # Erklärung hinzufügen
    add_explanation(c, data, margin, column_width, bottom_margin)

    # Python-Logo und Beschreibung hinzufügen
    add_logo_and_description(c, icons_folder, width, margin, bottom_margin)

    c.save()


def add_header(c, width, height, margin, user_name):
    """
    Fügt die Überschrift und die Trennline ein.
    """
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, height - margin - -15,
                 f"{user_name} Skill-Übersicht")
    c.line(margin, height - margin - -10,
           width - margin, height - margin - -10)


def draw_categories(
        c,
        data,
        icons_folder,
        height,
        width,
        margin,
        column_width
):
    """
    Zeichnet die Kategorien, deren Namen und Icons in das PDF.
    """
    y_position_left = height - margin - 1
    y_position_right = height - margin - 1

    # Variablen für die niedrigste Y-Position initialisieren
    min_y_left = height - margin - 1
    min_y_right = height - margin - 1

    left_categories = ["Hardware-Kenntnisse", "Arbeitsabläufe",
                       "Hardware-Reparatur"]
    right_categories = ["Softwaresysteme", "Software-Kenntnisse"]

    icon_params = set_icon_parameters(height=13, width=13, y_offset=3)

    for category, items in data.items():
        # Bestimme Position basierend auf der Kategorie
        if category in left_categories:
            y_position = y_position_left
            x_position = margin
        elif category in right_categories:
            y_position = y_position_right
            x_position = margin + column_width
        else:
            continue

        # Berechne die Breite des Textes
        text_width = c.stringWidth(category, "Helvetica-Bold", 14)

        # Kategorieüberschrift zeichnen (angepasste Breite)
        c.setFillColor(HexColor("#FFFACD"))  # Farbe für alle Kategorien
        c.rect(
            x_position - 2,          # Leicht über die Kategorie hinaus
            y_position - 10 - 2,     # Oberhalb der Kategorie
            text_width + 4,          # Breite basierend auf Textbreite
            15,                      # Höhe des Rechtecks
            stroke=0,                # Kein Rand
            fill=1                   # Füllen
        )

        # Kategorieüberschrift
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#000000"))
        c.drawString(x_position, y_position - 10, category)
        y_position -= 15

        # Einträge in der Kategorie
        for item in items:
            draw_item(
                c,
                item,
                x_position,
                y_position,
                icons_folder,
                icon_params
            )
            y_position -= 20

        # Aktualisiere die Y-Positionen für die Spalten
        if category in left_categories:
            y_position_left = y_position
            # Aktualisiere linke Spalte
            min_y_left = min(min_y_left, y_position)
        elif category in right_categories:
            y_position_right = y_position
            # Aktualisiere rechte Spalte
            min_y_right = min(min_y_right, y_position)

    # Füge die vertikale Linie in der Mitte hinzu
    center_x = width / 2
    c.setLineWidth(1)
    c.setStrokeColor(HexColor("#000000"))  # Schwarz
    c.line(center_x, height - margin, center_x, min(min_y_left, min_y_right))


def draw_item(c, item, x_position, y_position, icons_folder, icon_params):
    """
    Zeichnet einen einzelnen Eintrag mit Namen, Icons und Farben.
    """
    name = item["Name"]
    icon_path = os.path.join(
        icons_folder, item["Icon"]) if item["Icon"] else None
    color = get_color_for_value(item["Value"])
    num_icons = int(
        item["Value"]) if item["Value"] and item["Value"].isdigit() else 1

    # Namen zeichnen (links in der Spalte)
    c.setFillColor(HexColor("#000000"))
    c.setFont("Helvetica", 12)
    c.drawString(x_position + 5, y_position - 10, name)

    # Berechne die Position für die Symbole (rechts in der Spalte)
    if x_position < c._pagesize[0] / 2:  # Linke Spalte
        symbol_x_start = c._pagesize[0] / 2 - 20
    else:  # Rechte Spalte
        symbol_x_start = c._pagesize[0] - 50

    # Icons zeichnen (rechtsbündig)
    if icon_path and os.path.isfile(icon_path):
        try:
            for i in range(num_icons):
                icon_x_position = symbol_x_start - \
                    i * (icon_params["width"] + 9)
                c.setFillColor(color)
                c.rect(
                    icon_x_position - 2,
                    y_position - 15,
                    icon_params["width"] + 10,
                    icon_params["height"] + 3,
                    stroke=0,
                    fill=1,
                )
                c.drawImage(
                    icon_path,
                    icon_x_position,
                    y_position - 13,
                    width=icon_params["width"],
                    height=icon_params["height"],
                    mask="auto",
                )
        except Exception as e:
            print(f"Fehler bei Icon '{icon_path}': {e}")


def add_explanation(c, data, margin, column_width, bottom_margin):
    """
    Fügt die Erklärung mit farbigen Blöcken zum PDF hinzu.
    """
    explanation_x = margin + column_width
    explanation_y = bottom_margin + 200

    # Gelber Hintergrund für gesamte Erklärung
    num_items = len(data.get("Erklärung", []))
    explanation_box_height = 15 + num_items * 20  # Basis-Höhe + Einträge
    c.setFillColor(HexColor("#FFFACD"))  # Helles Gelb
    c.rect(
        explanation_x - 5,           # Links ausdehnen
        explanation_y - (num_items * 20) - -10,  # Bis zum letzten Eintrag
        235,                        # Breite des Rechtecks
        explanation_box_height - -15,     # Höhe dynamisch anpassen
        stroke=0,
        fill=1
    )

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(HexColor("#000000"))
    c.drawString(explanation_x, explanation_y + 20, "Erklärung")
    c.line(
        explanation_x,
        explanation_y + 18,
        explanation_x + c.stringWidth("Erklärung", "Helvetica-Bold", 15),
        explanation_y + 18,
    )

    c.setFont("Helvetica", 10)
    for item in data.get("Erklärung", []):
        name = item["Name"]
        color = get_color_for_value(item["Value"])
        c.setFillColor(color)
        c.rect(explanation_x, explanation_y, 225, 15, stroke=0, fill=1)
        c.setFillColor(HexColor("#000000"))
        c.drawString(explanation_x + 5, explanation_y + 3, name)
        explanation_y -= 20


def add_logo_and_description(c, icons_folder, width, margin, bottom_margin):
    """
    Fügt das Python-Logo, den QR-Code und die Beschreibung zum PDF hinzu.
    """
    # Pfad zum Python-Logo und QR-Code
    logo_path = os.path.join(icons_folder, "pl.png")
    qr_code_path = os.path.join(icons_folder, "qr_code.png")

    # Dimensionen des Logos
    logo_width = 100
    logo_height = 100
    qr_width = 100
    qr_height = 100

    # Startpositionen für das Logo und den QR-Code
    logo_x = width - margin - qr_width - logo_width - 20  # Platz QR rechts
    logo_y = bottom_margin + 10  # Abstand zum unteren Rand
    qr_x = logo_x + logo_width + 10  # Rechts neben dem Logo
    qr_y = logo_y  # Gleiche Höhe wie das Logo

    # Python-Logo hinzufügen
    if os.path.isfile(logo_path):
        try:
            c.drawImage(
                logo_path,
                logo_x,
                logo_y,
                width=logo_width,
                height=logo_height,
                mask="auto",
            )
        except Exception as e:
            print(f"Fehler beim Laden des Python-Logos: {e}")

    # QR-Code hinzufügen
    if os.path.isfile(qr_code_path):
        try:
            c.drawImage(
                qr_code_path,
                qr_x,
                qr_y,
                width=qr_width,
                height=qr_height,
                mask="auto",
            )
        except Exception as e:
            print(f"Fehler beim Laden des QR-Codes: {e}")

    # Beschreibungstext hinzufügen
    text = (
        "Dieses Dokument wurde von einem von mir geschriebenen Python-Skript "
        "erstellt. Scannen Sie den QR-Code, um direkt zu "
        "meinem GitHub-Repository unter "
        "www.github.com/Morn2/Skills zu gelangen. "
        "Skills.py ist die Datei des Sourcecodes. "
    )
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 12
    style.leading = 12  # Zeilenhöhe
    style.textColor = HexColor("#000000")

    # Text unter Logo + QR-Code
    text_x = logo_x  # Gleiche Startposition wie das Logo
    text_y = logo_y - 80  # Unter dem Logo und QR-Code
    text_width = logo_width + qr_width + 10  # Breite von Logo + QR-Code

    paragraph = Paragraph(text, style)
    # Breite und maximale Höhe des Textblocks
    paragraph.wrapOn(c, text_width, 50)
    paragraph.drawOn(c, text_x, text_y)


# Pfade und Dateinamen
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "daten.csv")
icons_folder = os.path.join(script_dir, "Icons")
output_pdf_path = os.path.join(script_dir,
                               "Skills Übersicht.pdf")

# CSV Lesen
data = read_data_from_csv(csv_file_path)

# Benutzername abfragen
user_name = get_user_name()

# PDF erstellen
create_pdf(output_pdf_path, data, icons_folder, user_name)
