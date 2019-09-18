"""
Extract PDF text using PDFMiner. Adapted from
http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

import io, re


def pdf_to_text(pdfname):

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()
    text = re.sub(r'\s', " ", text, flags=re.IGNORECASE)
    text = re.sub(r'  ', " ", text, flags=re.IGNORECASE)
    text = text.replace(" ", "")
    
    # Cleanup
    device.close()
    sio.close()

    return text
