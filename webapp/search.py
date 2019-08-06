import re
import string

import normalizeText
import pandas
from autocorrect import spell
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


class ResultElement:
    def __init__(self, rank, name, filename, score):
        self.rank = rank
        self.name = name
        self.filename = filename
        self.score = score

    def spellCorrect(string):
        words = string.split(" ")
        correctWords = []
        for i in words:
            correctWords.append(spell(i))
        return " ".join(correctWords)


def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def clearup(s, chars):
    return re.sub('[%s]' % chars, '', s).lower()


def normalize(words):
    words = words.lower()
    words = words.translate(str.maketrans({key: None for key in string.punctuation})) #remove punctuation
    words = words.strip() #remove white space
    words = normalizeText.remove_stopwords(words)
    words = normalizeText.replace_numbers(words) # replace number to words
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

    if len(r_optionalkey) != 0:
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
    print(df)

    resume = df['rawResume']
    resume_vect = []
    score = []
    for row in resume:

        t_resume = normalize(row)
        t_resume = ' '.join(t_resume)
        t_resume = t_resume.translate(str.maketrans('', '', string.punctuation))
        t_resume = str(t_resume)
        text_raw = str(row)
        try:
            tttt = summarize(text_raw, word_count=100)
            text = [tttt]
            vector = vectorizer.transform(text)
            resume_vect.append(vector.toarray())
        except Exception as e:
            print(e)
            pass
    df['Score'] = ''
    for i in resume_vect:
        samples = i
        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(samples)
        NearestNeighbors(algorithm='auto', leaf_size=30)
        scorea = neigh.kneighbors(Job_Desc_Imp)[0][0].tolist()
        if len(optionalkey) != 0:
            scoreb = neigh.kneighbors(Job_Desc_Opt)[0][0].tolist()
            score.append(scorea[0] * 0.7 + scoreb[0] * 0.3)
        else:
            score.append(scorea[0])

    df['Score'] = score
    df = df.sort_values(by=["Score"], ascending=False)
    df1 = df[['name','profileURL','Score']]
    # print(df1)

    flask_return = []

    rank = 0
    for idx, row in df1.head().iterrows():
        name = row['name']
        filename = row['profileURL']
        score = row['Score']
        rank = rank + 1
        res = ResultElement(rank, name, filename, score)
        flask_return.append(res)
        # # res.printresult()
        # print(f"Rank{res.rank+1} :\t {res.filename}")

    return flask_return
