import os
import pickle

import upload_resume
from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Resumes/'


def uploadFile(file):
    Filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], Filename))
    return Filename


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/createResumePage')
def createResumePage():
    return render_template('createResumePage.html')


@app.route('/uploadResumePage')
def uploadResumePage():
    return render_template('uploadResumePage.html')


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
    pickle.dump(experienceRaw, open('experience.pickle', "wb"))

    # rawResume can be searched by KNN like pdf, docx formats.
    # pdf, docx text should be saved into rawResume.
    rawResume = nameRaw + role + "\r\nmonthly salary: "
    monthlySalary + aboutRaw + experienceRaw + licensesCertificationsRaw + skillsEndorsementsRaw

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


@app.route('/searchResumeAction', methods=['POST'])
def searchResumeAction():
    # print(request.form)

    searchImportantKey = request.form['importantKey']
    searchOptionKey = request.form['optionKey']

    return render_template('searchResumePageResult.html', searchImportantKey=searchImportantKey,
                           searchOptionKey=searchOptionKey)


if __name__ == '__main__':
    app.run(debug=True)
