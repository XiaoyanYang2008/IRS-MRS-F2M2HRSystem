import pickle

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/createResumePage')
def createResumePage():
    return render_template('createResumePage.html')


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
    rawResume = nameRaw + roleRaw + "\r\nmonthly salary: "
    monthlySalary + aboutRaw + experienceRaw + licensesCertificationsRaw + skillsEndorsementsRaw

    return render_template('createResumePageResult.html', name=nameRaw)


if __name__ == '__main__':
    app.run(debug=True)
