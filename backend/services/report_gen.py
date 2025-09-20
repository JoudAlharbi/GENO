from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime

def build_pdf(local_path: str, report_id: str, results: dict):
    c = canvas.Canvas(local_path, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 16); c.drawString(25*mm, h-20*mm, "GENO — DNA Risk Report")
    c.setFont("Helvetica", 9)
    c.drawString(25*mm, h-26*mm, f"Report ID: {report_id}")
    c.drawString(25*mm, h-31*mm, f"Generated: {datetime.utcnow().isoformat()}Z")
    c.setFont("Helvetica-Bold", 12); c.drawString(25*mm, h-42*mm, "Summary")
    c.setFont("Helvetica", 11)
    c.drawString(25*mm, h-48*mm, f"Risk Level: {results.get('risk_level')}")
    c.drawString(25*mm, h-54*mm, f"Score: {results.get('score')}")
    y = h-72*mm; c.setFont("Helvetica-Bold", 12); c.drawString(25*mm, y, "Detected Markers")
    y -= 6*mm; c.setFont("Helvetica", 10)
    for m in results.get("markers", []):
        line = f"- {m.get('gene')} | {m.get('variant')} | {m.get('locus')} | ACMG:{m.get('acmg','N/A')} | Evidence:{m.get('evidence','N/A')}"
        c.drawString(30*mm, y, line[:120]); y -= 6*mm
        if y < 25*mm: c.showPage(); y = h-25*mm
    c.save()