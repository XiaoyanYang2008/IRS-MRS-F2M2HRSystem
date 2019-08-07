import re
import string

import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

import normalizeText


class ResultElement:
    def __init__(self, rank, name, filename, score):
        self.rank = rank
        self.name = name
        self.filename = filename
        self.score = score


def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp


def clearup(s, chars):
    return re.sub('[%s]' % chars, '', s).lower()


def normalize(words):
    words = words.lower()
    words = normalizeText.replace_numbers(words)  # replace number to words
    words = words.translate(str.maketrans({key: None for key in string.punctuation})) #remove punctuation
    words = words.strip() #remove white space
    words = normalizeText.remove_stopwords(words)
    words = normalizeText.remove_non_ascii(words)
    words = normalizeText.lemmatize_verbs(words)
    return words


def res(importantkey, optionalkey):
    normalizeText.denoise_text(importantkey)
    normalizeText.denoise_text(optionalkey)
    importantkey = normalize(importantkey)
    optionalkey = normalize(optionalkey)

    try:
        impt = str(importantkey)
        textimp = [impt]
    except:
        textimp = 'None'

    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(textimp)
    vector = vectorizer.transform(textimp)

    Job_Desc_Imp = vector.toarray()

    if len(optionalkey) != 0:
        try:
            optt = str(optionalkey)
            textopt = [optt]
            vectorizerOpt = TfidfVectorizer(stop_words='english')
            vectorizerOpt.fit(textopt)
            vectorOpt = vectorizer.transform(textopt)
            Job_Desc_Opt = vectorOpt.toarray()
        except:
            textopt = 'None'

    df = pandas.read_csv("./db/resume_db.csv")


    resume = df['rawResume']
    resume_vect = []
    resume_vect_Raw = []

    score_A = []
    score_B = []
    for row in resume:
        t_raw = str(row)
        try:
            text = normalize(t_raw)
            t_resume = ' '.join(text)
            t_resume = t_resume.translate(str.maketrans('', '', string.punctuation))
            text = [t_resume]
            vector_raw = vectorizer.transform(text)
            resume_vect_Raw.append(vector_raw.toarray())
            vector = vectorizer.transform(text)
            resume_vect.append(vector.toarray())
        except Exception as e:
            print(e)
            pass

    for i in resume_vect:
        samples = i
        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(samples)
        NearestNeighbors(algorithm='auto', leaf_size=30)
        scorea = neigh.kneighbors(Job_Desc_Imp)[0][0].tolist()
        score_A.append(scorea[0])
        if len(optionalkey) != 0:
            scoreb = neigh.kneighbors(Job_Desc_Opt)[0][0].tolist()
            score_B.append(scoreb[0])

    df['Score_A'] = score_A

    if len(optionalkey) != 0:
        df['Score_B'] = score_B
        df['Score'] = df['Score_A'] * 0.7 + df['Score_B'] * 0.3
    else:
        df['Score'] = df['Score_A']

    df = df.sort_values(by=["Score"])
    df1 = df[['name','profileURL','Score']]

    flask_return = []

    rank = 0
    for idx, row in df1.head(20).iterrows():
        name = row['name']
        filename = row['profileURL']
        score = row['Score']
        rank = rank + 1
        res = ResultElement(rank, name, filename, score)
        flask_return.append(res)

    return flask_return
