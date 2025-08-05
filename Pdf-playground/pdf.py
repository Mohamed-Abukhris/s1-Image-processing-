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