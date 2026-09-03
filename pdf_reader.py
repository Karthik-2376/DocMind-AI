from PyPDF2 import PdfReader
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    pages = []
    for page_num,page in enumerate(pdf_reader.pages,start=1):
        text = page.extract_text()
        if text and text.strip():
            pages.append({"page": page_num,"text": text})
    if not pages:
        raise ValueError("No text found in the PDF.")

    return pages