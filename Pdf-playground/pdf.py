import PyPDF2

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