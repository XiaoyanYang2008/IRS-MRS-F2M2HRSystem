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
    name = request.form['name']
    profileURL = request.form['profileURL']
    role = request.form['role']
    monthlySalary = request.form['monthlySalary']
    about = request.form['about']
    experience = request.form['experience']
    education = request.form['education']
    licensesCertifications = request.form['licensesCertifications']
    skillsEndorsements = request.form['skillsEndorsements']


    return render_template('createResumePageResult.html', name=name)

if __name__ == '__main__':
    app.run(debug = True)