import os
import warnings
import csv
import PyPDF2
from docx import Document

def insertResume(name, profileURL, rawContent):
    # Insert resume into ./db/resume_db.csv
    try:
        resumeheader = ['name', 'profileURL', 'rawResume']
        resumeList = [name, profileURL, rawContent]

        if not os.path.exists('./db/resume_db.csv'):
            with open("./db/resume_db.csv", "w") as tmp:
                wh = csv.writer(tmp, quoting=csv.QUOTE_NONE)
                wh.writerow(resumeheader)
                tmp.close()

        with open("./db/resume_db.csv", "a+") as fp:
            wr = csv.writer(fp, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(resumeList)

        return "Resume of " + name + " created successfully"
    except Exception as e:
        errmsg = "Error encountered: " + str(e)
        return errmsg


def extractResumeContent(filename):
    file = "./Resumes/" + filename
    Resumes = []
    Temp_pdf = []

    Temp = filename.split(".")
    if Temp[1].lower() == "pdf":
        print("This is PDF - ", filename)
        try:
            with open(file, 'rb') as pdf_file:
                read_pdf = PyPDF2.PdfFileReader(pdf_file)
                number_of_pages = read_pdf.getNumPages()
                for page_number in range(number_of_pages):
                    page = read_pdf.getPage(page_number)
                    page_content = page.extractText()
                    page_content = page_content.replace('\n', ' ')
                    Temp_pdf = str(Temp_pdf) + str(page_content)
                Resumes.extend([Temp_pdf])
                Temp_pdf = ''
        except Exception as e:
            print(e)

    elif Temp[1].lower() == "docx":
        print("This is DOCX - ", filename)
        try:
            doc = Document(file)
            txt = []
            for para in doc.paragraphs:
                txt.append(para.text)
            Resumes = ' '.join(txt)
        except Exception as e:
            print(e)

    else:
        print("Unknown File Extension: ", file)
        pass

    return Resumes
