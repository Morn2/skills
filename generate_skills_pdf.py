from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import utils

def create_document(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Überschrift hinzufügen und unterstreichen
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Aaron Feldmann Skill Auflistung")
    c.line(100, height - 55, width - 100, height - 55)  # Unterstrich hinzufügen

    # Beispiel-Daten
    data = {
        "Hardware": [("Löten", "Icons/Löten.png", 2), ("SMD Löten", "Icons/SMD Löten.png", 3)],
        "Software": [("Apple IOS", "Icons/Apple IOS.png", 1), ("Android", "Icons/Android.png", 1)]
    }

    y_position = height - 100

    for category, items in data.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, category)
        y_position -= 20

        for name, icon_path, value in items:
            try:
                c.setFont("Helvetica", 12)
                c.drawString(100, y_position, f"{name} ({value})")
                
                # Hintergrund weiß setzen
                icon = utils.ImageReader(icon_path)
                icon_width, icon_height = icon.getSize()
                aspect = icon_height / float(icon_width)
                icon_width = 1.5 * cm
                icon_height = icon_width * aspect

                c.setFillColorRGB(1, 1, 1)
                c.rect(250, y_position - icon_height, icon_width, icon_height, fill=1)
                c.drawImage(icon_path, 250, y_position - icon_height, width=icon_width, height=icon_height)
                
                y_position -= (icon_height + 10)
            except IOError:
                c.setFont("Helvetica", 12)
                c.drawString(100, y_position, f"{name} ({value}) - Icon not found")
                y_position -= 20

        y_position -= 20  # Leerschlag zwischen Kategorien

    c.save()

create_document("skills.pdf")
