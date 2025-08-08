import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas     #Generate a 1-page PDF with a logo image
from reportlab.lib.pagesizes import letter
import io   #Handle the temporary PDF in memory (no file writing)

pdf_files= [
    "dummy.pdf",
    "twopage.pdf",
    "wtr.pdf"
]

def pdf_combiner(pdf_list):
    merger = PyPDF2.PdfFileMerger()
    for pdf in pdf_list:
        print(f"Adding {pdf}")
        merger.append(open(pdf,'rb'))
    with open('super.pdf', 'wb') as fo:
        merger.write(fo)
    print("Merged pdf saved as super.pdf")

pdf_combiner(pdf_files)

template = PyPDF2.PdfFileReader(open('super.pdf', 'rb'))
watermark = PyPDF2.PdfFileReader(open('wtr.pdf', 'rb'))
output = PyPDF2.PdfFileWriter()


for i in range(template.getNumPages()):
    page = template.getPage(i)
    page.mergePage(watermark.getPage(0))
    output.addPage(page)

with open('watermarked_output.pdf', 'wb') as outputFile:
    output.write(outputFile)

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawImage("logowa.png", 450, 750, width=100, height=50)  # Adjust position and size
can.save()

packet.seek(0)
logo_pdf = PdfFileReader(packet)

existing_pdf = PdfFileReader(open("super.pdf", "rb"))
output = PdfFileWriter()

for i in range(existing_pdf.getNumPages()):
    page = existing_pdf.getPage(i)
    page.mergePage(logo_pdf.getPage(0))
    output.addPage(page)


with open("output_with_logo.pdf", "wb") as outputStream:
    output.write(outputStream)
