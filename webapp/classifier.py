import re
import numpy as np
import pandas as pd
import warnings
import PyPDF2
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer



def extract_text_from_pdf(pdf_file):
    pdfreader = PyPDF2.PdfFileReader(open(pdf_file,'rb'))
    pdf_content = ""
    for page in range(0,pdfreader.getNumPages()):
        pdfpage = pdfreader.getPage(page)
        pdf_content = pdf_content + pdfpage.extractText()
    return cleanResume((pdf_content))


class resumeClassifier():
    def __init__(self):
        self.model,self.label_encoder,self.vectoriser = get_trainedModel()

def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)
    resumeText = re.sub('RT|cc', ' ', resumeText)
    resumeText = re.sub('#\S+', '', resumeText)
    resumeText = re.sub('@\S+', '  ', resumeText)
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

def get_trainedModel():
    resumeDataSet = pd.read_csv('UpdatedResumeDataSet.csv', encoding='utf-8')
    resumeDataSet['cleaned_resume'] = ''
    resumeDataSet['cleaned_resume'] = resumeDataSet.Resume.apply(lambda x: cleanResume(x))

    var_mod = ['Category']
    le = LabelEncoder()
    for i in var_mod:
        resumeDataSet[i] = le.fit_transform(resumeDataSet[i])

    requiredText = resumeDataSet['cleaned_resume'].values
    requiredTarget = resumeDataSet['Category'].values

    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        stop_words='english',
        max_features=1500)
    word_vectorizer.fit(requiredText)
    WordFeatures = word_vectorizer.transform(requiredText)

    clf = OneVsRestClassifier(KNeighborsClassifier())
    clf.fit(WordFeatures, requiredTarget)
    return clf,le,word_vectorizer

    # prediction = clf.predict(X_test)