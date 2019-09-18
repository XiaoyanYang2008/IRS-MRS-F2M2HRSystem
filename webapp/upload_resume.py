import os
import warnings
import csv
import pdf2text
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

    Temp = filename.split(".")
    if Temp[1].lower() == "pdf":
        print("This is PDF - ", filename)
        try:
            Resumes = pdf2text.pdf_to_text(file)
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
