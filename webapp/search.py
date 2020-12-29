import re
import string

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

import app_constants
import lk_parser
import normalizeText


class ResultElement:
    def __init__(self, rank, name, filename, score, type):
        self.rank = rank
        self.name = name
        self.filename = filename
        self.score = score
        self.type = type


def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp


def clearup(s, chars):
    return re.sub('[%s]' % chars, '', s).lower()


def normalize(words):
    words = words.lower()
    words = normalizeText.replace_numbers(words)  # replace number to words
    words = words.translate(str.maketrans({key: None for key in string.punctuation}))  # remove punctuation
    words = words.strip()  # remove white space
    words = normalizeText.remove_stopwords(words)
    words = normalizeText.remove_non_ascii(words)
    words = normalizeText.lemmatize_verbs(words)
    words = ' '.join(words)
    return words


hasA = 'noA'
hasB = 'noB'


def gethasA():
    return hasA


def gethasB():
    return hasB


def ui_search(important_search):
    global hasA
    df1 = search_by_tfidf(important_search)
    # print(df1)

    flask_return = []

    rank = 0
    for idx, row in df1.head(20).iterrows():
        name = row['name']
        filename = row['profileURL']
        score = row['NScore']
        rank = rank + 1
        flask_return.append(ResultElement(rank, name, filename, score, 'typeA'))
        hasA = 'hasA'
        
    # for idx, row in df1.head(20).iterrows():
    #     name = row['name']
    #     filename = row['profileURL']
    #     score = row['NScore']
    #     if (score <= 1 and score > 0.75):
    #         type = 'typeA'
    #         hasA = 'hasA'
    #     elif (score <0.75):
    #         type = 'typeB'
    #         hasB = 'hasB'
    #     else:
    #         type = 'noType'
    #     rank = rank + 1
    #     res = ResultElement(rank, name, filename, score, type)
    #     flask_return.append(res)
    return flask_return


def search_by_tfidf(search_keywords):
    search_keywords = normalize(search_keywords)
    resume_df = pd.read_csv("./db/resume_db.csv")
    resume_df.drop_duplicates(subset="profileURL",
                              keep='last', inplace=True)
    resumes = resume_df['rawResume']
    resume_sm, tfidf_vectorizer = build_tfidf_vectorizer(resumes)
    search_sm = tfidf_vectorizer.transform([search_keywords])
    vals = cosine_similarity(search_sm, resume_sm)
    df = resume_df
    df['Score'] = vals[0]
    df = df[df['Score'] != 0]

    if(len(df)==0):
        return df
    
    if max(df['Score'] != 0):
        df['NScore'] = df['Score'] / max(df['Score'])  # rescale for optaPlanner planning
    else:
        df['NScore'] = df['Score']

    # idx = vals.argsort()[0][-1]
    #
    # print(type(vals))
    # print(resumeDF.iloc[[idx]])
    df = df.sort_values(by=["Score"], ascending=False)
    db = lk_parser.loadData(app_constants.RESUMEDB_FILE_PB)
    df['expectedMonthlySalary'] = df['profileURL'].apply(lambda x: getExpectMonthlySalary(db, x))

    df1 = df[['name', 'profileURL', 'Score', 'NScore', 'expectedMonthlySalary']]
    # df1 = df
    return df1


def getExpectMonthlySalary(db, x):
    resume = lk_parser.findResumeByURL(db, x)
    if resume is not None:
        return resume.monthlySalary
    else:
        return 0


def build_tfidf_vectorizer(resumes):
    resumes = resumes.apply(normalize)
    # TODO: search keywords can be comma seperated, input this method to see what result matched what keywords.
    #  May help to explain results matched with which keywords, as long as none zero.
    # Example, zaki matched java, but other people doesn't matched java. so, java keywords under zaki has a score

    tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_vectorizer.fit(resumes.tolist())
    resume_sm = tfidf_vectorizer.transform(resumes.tolist())
    return resume_sm, tfidf_vectorizer


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

    df = pd.read_csv("./db/resume_db.csv")
    df.drop_duplicates(subset="profileURL",
                       keep='last', inplace=True)

    resume = df['rawResume']
    resume_vect = []
    resume_vect_Raw = []

    score_A = []
    score_B = []
    for row in resume:
        t_raw = str(row)
        try:
            t_resume = normalize(t_raw)
            # t_resume = ' '.join(text) # done in normalize()
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
    df1 = df[['name', 'profileURL', 'Score']]
    print(df1)
    flask_return = []

    rank = 0
    global hasA
    global hasB
    for idx, row in df1.head(20).iterrows():
        name = row['name']
        filename = row['profileURL']
        score = row['Score']
        if score < 1:
            type = 'typeA'
            hasA = 'hasA'
        elif (score >= 1 and score < 2):
            type = 'typeB'
            hasB = 'hasB'
        else:
            type = 'noType'
        rank = rank + 1
        res = ResultElement(rank, name, filename, score, type)
        flask_return.append(res)
    return flask_return
