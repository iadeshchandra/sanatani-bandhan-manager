import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

def get_report_dir():
    if 'ANDROID_STORAGE' in os.environ:
        path = '/storage/emulated/0/Documents/Sanatani_Reports/'
    else:
        path = os.path.join(os.getcwd(), 'Sanatani_Reports')
        
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def generate_donation_report(data):
    path = get_report_dir()
    filename = os.path.join(path, f"Daan_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
    
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Sanatani Bandhan - Daan (Donation) Report")
    c.setFont("Helvetica", 12)
    
    y = 760
    total = 0
    for row in data:
        c.drawString(50, y, f"Date: {row[3]} | Donor: {row[1]} | Amount: {row[2]}")
        total += float(row[2])
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
            
    c.drawString(50, y-20, f"Total Daan: {total}")
    c.save()
    return filename
