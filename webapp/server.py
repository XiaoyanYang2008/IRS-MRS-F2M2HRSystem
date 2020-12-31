import os

import nltk
from flask import (Flask, render_template, request,
                   send_from_directory, jsonify)
from werkzeug import secure_filename

import app_constants
import classifier
import lk_parser
import resumeDB_pb2
import search
import upload_resume
from lk_parser import findResumeByURL

SECTION_SEPERATOR = " \r\n"
classifierModel = classifier.resumeClassifier()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Resumes/'


def uploadFile(file):
    Filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], Filename))
    return Filename


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resources/<path:path>')
def send_resources(path):
    return send_from_directory('resources', path)


@app.route('/createResumePage')
def createResumePage():
    return render_template('createResumePage.html', resume=resumeDB_pb2.Resume())


@app.route('/uploadResumePage')
def uploadResumePage():
    return render_template('uploadResumePage.html')


@app.route('/classifier')
def classifierPage():
    return render_template('classifier.html')


@app.route('/editResume')
def editResume():
    profileURL = request.args.get('profileURL')
    db = lk_parser.loadData(app_constants.RESUMEDB_FILE_PB)
    resume = findResumeByURL(db, profileURL)

    return render_template('createResumePage.html', resume=resume)


@app.route('/createResumeAction', methods=['POST'])
def createResumeAction():
    # print(request.form)

    nameRaw = request.form['name']
    profileURL = request.form['profileURL']
    role = request.form['role']
    monthlySalary = request.form['monthlySalary']
    aboutRaw = request.form['about']
    experienceRaw = request.form['experience']
    educationRaw = request.form['education']
    licensesCertificationsRaw = request.form['licensesCertifications']
    skillsEndorsementsRaw = request.form['skillsEndorsements']
    # pickle.dump(experienceRaw, open('experience.pickle', "wb"))
    # pickle.dump(educationRaw, open('education.pickle', "wb"))

    # rawResume can be searched by KNN like pdf, docx formats.
    # pdf, docx text should be saved into rawResume.
    rawResume = nameRaw + SECTION_SEPERATOR + role + SECTION_SEPERATOR + "monthlysalary: " \
        + monthlySalary + SECTION_SEPERATOR + aboutRaw + SECTION_SEPERATOR + \
        experienceRaw + SECTION_SEPERATOR + licensesCertificationsRaw + SECTION_SEPERATOR + \
        skillsEndorsementsRaw

    try:
        uploadfile = request.files['uploadfile']
    except:
        uploadfile = None

    if uploadfile:
        result = uploadFile(uploadfile)
        URL = result
    else:
        URL = profileURL

    result = upload_resume.insertResume(nameRaw, URL, rawResume)

    # For protobuf DB.
    db = lk_parser.loadData(app_constants.RESUMEDB_FILE_PB)
    resume = findResumeByURL(db, profileURL)
    if resume is None:
        resume = resumeDB_pb2.Resume()

    resume.name = nameRaw
    resume.profileURL = profileURL
    resume.rawResume = rawResume
    resume.monthlySalary = float(monthlySalary)

    if role.find(' at ') != -1:
        resume.companyName = role.split(" at ")[1]
        resume.title = role.split(" at ")[0]

    resume.aboutRaw = aboutRaw
    resume.educationRaw = educationRaw
    resume.educations.extend(lk_parser.extractEducations(educationRaw))
    resume.experienceRaw = experienceRaw
    resume.experiences.extend(lk_parser.extractExperiences(experienceRaw))
    resume.licensesCertificationsRaw = licensesCertificationsRaw
    resume.skillsEndorsementsRaw = skillsEndorsementsRaw

    resumeExists = findResumeByURL(db, profileURL)
    if resumeExists is None:
        db.resumes.append(resume)

    lk_parser.saveData(app_constants.RESUMEDB_FILE_PB, db)

    return render_template('createResumePageResult.html', results=result)


@app.route('/uploadResumeAction', methods=['POST'])
def uploadResumeAction():
    name = request.form['name']
    # Following code is to upload resume file to server
    try:
        uploadfile = request.files['uploadfile']
    except:
        uploadfile = None

    if uploadfile:
        uploadfilename = uploadFile(uploadfile)
        rawResume = upload_resume.extractResumeContent(uploadfilename)
        result = upload_resume.insertResume(name, uploadfilename, rawResume)
    else:
        result = "No Profile to upload"

    return render_template('createResumePageResult.html', results=result)


@app.route('/searchResumePage')
def searchResumePage():
    return render_template('searchResumePage.html')


@app.route('/searchResumeAction', methods=['POST', 'GET'])
def searchResumeAction():
    # print(searchresult.form)

    searchImportantKey = request.form['importantKey']
    algorithm_type = request.form['algorithmType']
    try:
        searchImportantKey = request.form['importantKey']
    except:
        searchImportantKey = None

    searchOptionKey = request.form['optionKey']

    if searchImportantKey:

        if "KNN" == algorithm_type:
            result = search.res(searchImportantKey, searchOptionKey)
        elif "cosinesim" == algorithm_type:
            result = search.ui_search(searchImportantKey)

        hasA = search.gethasA()
        hasB = search.gethasB()
        return render_template('searchResumePageResult.html', results=result, hasA=hasA, hasB=hasB)
    else:
        result = "No 'Mandatory Search Key' input"
        return render_template('searchResumePageResult.html', results=result)


@app.route('/resumeSubmit', methods=['GET', 'POST'])
def get_resume():
    # data = json.dumps(request.form)
    print(request.files['resumes'])
    resumes = []
    for name, file in request.files.items():
        filename = uploadFile(file)
        resume = classifier.extract_text_from_pdf(
            app.config['UPLOAD_FOLDER']+filename)
        info = classifierModel.label_encoder.classes_[classifierModel.model.predict(
            classifierModel.vectoriser.transform([resume]))]
        resumes.append((filename, info))

    return render_template('classifierResult.html', results=resumes)


@app.route('/Resumes/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Resumes', filename)


@app.route('/api_search', methods=['GET', 'POST'])
def api_search():
    search_keywords = request.form['search']
    result_df = search.search_by_tfidf(search_keywords)
    result_df = result_df[result_df['profileURL'].str.contains('https://')]

    return jsonify(result_df.to_csv())


if __name__ == '__main__':
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    app.run(host='0.0.0.0', port=5000, debug=True)
