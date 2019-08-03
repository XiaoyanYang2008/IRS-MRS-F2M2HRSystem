import re, string
import os
import pandas
import normalizeText
from bs4 import BeautifulSoup
from autocorrect import spell
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


class ResultElement:
    def __init__(self, rank, name, filename):
        self.rank = rank
        self.name = name
        self.filename = filename

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

    if optionalkey != '':
        try:
            optt = str(optionalkey)
            textopt = [optt]
        except:
            textopt = 'None'

    vectorizerOpt = TfidfVectorizer(stop_words='english')
    vectorizerOpt.fit(textopt)
    vectorOpt = vectorizer.transform(textopt)

    Job_Desc_Opt = vectorOpt.toarray()

    savedPath = os.getcwd()
    os.chdir('./db')
    df = pandas.read_csv("resume_db.csv")
    print(df)

    resume = df['rawResume']
    resume_vect = []
    score = []
    for row in resume:
        text = str(row)
        try:
            tttt = summarize(text, word_count=100)
            text = [tttt]
            vector = vectorizer.transform(text)
            resume_vect.append(vector.toarray())
        except:
            pass
    df['Score'] = ''
    for i in resume_vect:
        samples = i
        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(samples)
        NearestNeighbors(algorithm='auto', leaf_size=30)
        scorea = neigh.kneighbors(Job_Desc_Imp)[0][0].tolist()
        if optionalkey != '':
            scoreb = neigh.kneighbors(Job_Desc_Opt)[0][0].tolist()
            score.append(scorea[0] * 0.7 + scoreb[0] * 0.3)
        else:
            score.append(scorea[0])

    df['Score'] = score
    df = df.sort_values(by=["Score"], ascending=False)

    flask_return = []
    for row in df:
            print(row[1])
    for row in df:
            print(row[2])
    for row in df:
            print(row[3])

    # for i in enumerate(df):
        # print("Rank\t" , n+1, ":\t" , i)
        # flask_return.append(str("Rank\t" , n+1, ":\t" , i))
        # n = i
        # name = df[i]
        # filename = df[i][2]
        # #name = name.split('.')[0]
        # rank = i+1
        # res = ResultElement(rank, name, filename)
        # flask_return.append(res)
        # # res.printresult()
        # print(f"Rank{res.rank+1} :\t {res.filename}")

    os.chdir(savedPath)
    return flask_return
