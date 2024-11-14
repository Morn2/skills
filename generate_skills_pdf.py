from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_document(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Hier fügen wir später die Kategorien und Namen hinzu
    c.drawString(100, height - 100, "Kategorie 1")

    c.save()

create_document("skills.pdf")
