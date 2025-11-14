# transport_app/pdf_utils.py
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from django.conf import settings

def generate_epass_pdf(emp):
    # ---------- PDF PATH ----------
    folder = os.path.join(settings.MEDIA_ROOT, "epass")
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"EPASS_{emp.pass_no}.pdf")

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # ---------- CARD POSITION ----------
    card_x = 80
    card_y = 50
    card_w = 360
    card_h = 680

    # ---------- CARD BORDER ----------
    c.setLineWidth(1.2)
    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    c.rect(card_x, card_y, card_w, card_h)

    # ---------- RED SHIFT BAR ----------
    red_bar_w = 70
    c.setFillColorRGB(0.9, 0.1, 0.1)
    c.rect(card_x + card_w - red_bar_w, card_y, red_bar_w, card_h, fill=1)

    # TEXT ON RED BAR
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 18)
    c.translate(card_x + card_w - (red_bar_w / 2), card_y + (card_h / 2))
    c.rotate(90)
    c.drawCentredString(0, 0, "GENERALSHIFT")
    c.restoreState()

    # ---------- LOGO ----------
    logo_path = os.path.join(settings.BASE_DIR, "transport_app/static/images/logo.png")
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(
            logo,
            card_x + 95,
            card_y + card_h - 140,
            width=170,
            height=70,
            preserveAspectRatio=True,
            mask="auto"
        )

    # ---------- Fields Layout ----------
    base_y = card_y + card_h - 200
    line_gap = 35

    c.setFillColorRGB(0, 0, 0)

    # PASS NUMBER (show pass_no)
    c.setFont("Helvetica-Bold", 13)
    pass_no_display = emp.pass_no if getattr(emp, "pass_no", None) else "—"
    c.drawString(card_x + 20, base_y, f"No. {pass_no_display}")

    # Label + Line Helper
    def label_and_line(label, value, y):
        c.setFont("Helvetica-Bold", 13)
        c.drawString(card_x + 20, y, label)

        # underline line
        c.setLineWidth(1)
        c.line(card_x + 135, y - 2, card_x + card_w - 90, y - 2)

        # value
        c.setFont("Helvetica", 12)
        c.drawString(card_x + 138, y, value)

    # ---------- FIELD VALUES ----------
    pickup = emp.pickup_drop_point.name if emp.pickup_drop_point else "—"
    # Use pickup for both pickup/drop point (single field)
    y = base_y - 50
    label_and_line("Name:", emp.name or "—", y)

    y -= line_gap
    label_and_line("EID No.:", emp.emp_id or "—", y)

    y -= line_gap
    label_and_line("Entity:", emp.entity or "—", y)

    y -= line_gap
    label_and_line("Pickup/Drop Point:", pickup, y)   # <-- single combined field

    # ---------- BUS PASS BUTTON ----------
    btn_w = 150
    btn_h = 40
    btn_x = card_x + (card_w - red_bar_w - btn_w) / 2
    btn_y = card_y + 80

    c.setLineWidth(2)
    c.setStrokeColorRGB(0, 0, 0)
    c.rect(btn_x, btn_y, btn_w, btn_h)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(btn_x + btn_w/2, btn_y + 12, "BUS PASS")

    c.save()
    return file_path
