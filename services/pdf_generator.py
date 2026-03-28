import os
from fpdf import FPDF
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
    
    pdf = FPDF(format='A4')
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Sanatani Bandhan - Daan (Donation) Report", ln=True, align='C')
    pdf.cell(200, 10, txt="", ln=True) # spacer
    
    # Body
    pdf.set_font("Arial", size=12)
    total = 0
    for row in data:
        line = f"Date: {row[3]} | Donor: {row[1]} | Amount: {row[2]}"
        pdf.cell(200, 10, txt=line, ln=True)
        total += float(row[2])
            
    # Footer
    pdf.cell(200, 10, txt="", ln=True) # spacer
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt=f"Total Daan: {total}", ln=True)
    
    pdf.output(filename)
    return filename
