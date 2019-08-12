import pickle
import re

import resumeDB_pb2

SECTION_EDUCATION_TOKEN = "Education\r\n"
SECTION_EDUCATION_DEGREE_NAME_TOKEN = "Degree Name"

SECTION_EXPERIENCE_TOKEN = "Experience\r\n"
SECTION_EXPERIENCE_COMPANY_NAME_TOKEN = "Company Name"


def main():
    # main_testExperience()
    # main_testYearMonthTextToIntMonths()
    main_testEducation()


def main_testYearMonthTextToIntMonths():
    result = parseNumberOfMonth("2 yrs 9 mos")
    if (result != 33):
        print("ERROR 33")

    result = parseNumberOfMonth("8 mos")
    if (result != 8):
        print("ERROR 8")

    result = parseNumberOfMonth("1 yr 7 mos")
    if (result != 19):
        print("ERROR 19")

    result = parseNumberOfMonth("4 yrs")
    if (result != 48):
        print("ERROR 48")

    print("OK")
    return


def parseNumberOfMonth(yearMonthString):
    # "2 yrs 9 mos" => 2*12+9 => 33 months
    # "1 yr 7 mos" => 1*12+7 => 19 months

    yearMonthString = yearMonthString.strip()
    yearMonthString = yearMonthString.replace(" mos", "")
    yearMonthString = yearMonthString.replace(" mo", "")
    yearMonthString = yearMonthString.replace("yrs", "yr")

    year_month_array = yearMonthString.split(" yr")

    if len(year_month_array) == 1:
        return parseInt(year_month_array[0])
    else:
        return parseInt(year_month_array[0]) * 12 + parseInt(year_month_array[1])


def parseInt(str):
    if str is None or len(str) == 0:
        return 0
    else:
        return int(str)


def main_testExperience():
    experienceText = pickle.load(open('experience.pickle', 'rb'))
    print(experienceText)
    print('After processing....')

    resume = resumeDB_pb2.Resume()
    resume.experiences.extend(extractExperiences(experienceText))

    db = resumeDB_pb2.ResumeDB()
    db.resumes.append(resume)
    saveData("data.pb", db)


def main_testEducation():
    educationText = pickle.load(open('education.pickle', 'rb'))
    print(educationText)
    print('After processing....')

    resume = resumeDB_pb2.Resume()
    resume.educations.extend(extractEducations(educationText))

    db = resumeDB_pb2.ResumeDB()
    db.resumes.append(resume)
    saveData("data.pb", db)


def extractExperiences(experiencesText):
    records = experiencesText.split('\r\n\r\n')
    cnRecords = experiencesText.split(SECTION_EXPERIENCE_COMPANY_NAME_TOKEN)

    exps = []

    # TODO do UI check when extra empty lines more then company? 8 vs 8 in this case.
    print("length by 1 emptyline %s, by cn %s" % (len(records), len(cnRecords)))

    if (not records[0].startswith(SECTION_EXPERIENCE_TOKEN)):
        return

    for e in records:
        if (e.find(SECTION_EXPERIENCE_COMPANY_NAME_TOKEN) != -1):
            exps.append(extractAnExperienceData(e))

    # anExperience = extractAnExperienceData(records[0])

    # print(records)
    print("exps length:", len(exps), '\r\n\r\n')
    return exps


# TODO parse education field.
# check 'Degree name' count and \r\n\r\n split count first, TODO may need to do that as web validation.
#
def extractEducations(educationText):
    # print('educationText\r\n', educationText)
    records = educationText.split('\r\n\r\n')

    edus = []

    # TODO do UI check when extra empty lines more then company? 8 vs 8 in this case.
    # print("length by 1 emptyline %s, by cn %s" % (len(records), len(cnRecords)))

    if (not records[0].startswith(SECTION_EDUCATION_TOKEN)):
        return

    for e in records:
        if (e.find(SECTION_EDUCATION_DEGREE_NAME_TOKEN) != -1):
            edus.append(extractAnEducationData(e))

    # anExperience = extractAnExperienceData(records[0])

    # print(records)
    print("edus length:", len(edus), '\r\n\r\n')
    return edus


# Done regex. Done build domain class for structure data.
def extractAnExperienceData(anExperience):
    if (anExperience.startswith(SECTION_EXPERIENCE_TOKEN)):
        anExperience = anExperience.replace(SECTION_EXPERIENCE_TOKEN, "")

    # sections = anExperience.split("\r\n")
    print(anExperience)
    exp = resumeDB_pb2.Experience()
    exp.title = locateData("(.*)\r\n" + SECTION_EXPERIENCE_COMPANY_NAME_TOKEN, anExperience)

    # Title
    print(exp.title)

    # Titles for multiple titles within a company.
    # print(re.search("\r\nTitle(.*)\r\n", anExperience).group(1))

    # Company
    exp.companyName = locateData("\r\n" + SECTION_EXPERIENCE_COMPANY_NAME_TOKEN + "(.*)\r\n", anExperience)
    # print(exp.companyName)

    # Dates Employed
    exp.datesEmployedText = locateData("\r\nDates Employed(.*)\r\n", anExperience)

    # Employment Duration
    exp.employmentDurationText = locateData("\r\nEmployment Duration(.*)\r\n", anExperience)
    exp.employmentDurationInMonths = parseNumberOfMonth(exp.employmentDurationText)

    # Location search
    exp.location = locateData("\r\nLocation(.*)\r\n", anExperience)
    # print(exp.location)

    # experienceText
    # p = re.compile("\r\nLocation(.*)See [less|more]", re.DOTALL)
    # print(p.search(anExperience).group(1))

    exp.experienceText = locateData("\r\nLocation(.*)\r\n", anExperience, re.DOTALL)

    return exp


def extractAnEducationData(anEducationText):
    # if anEducationText.startswith(SECTION_EDUCATION_TOKEN):
    #     anEducationText = anEducationText.replace(SECTION_EDUCATION_TOKEN, "")

    # sections = anExperience.split("\r\n")

    print(anEducationText)

    edu = resumeDB_pb2.Education()
    edu.schoolName = locateData("\r\n(.*)\r\n" + SECTION_EDUCATION_DEGREE_NAME_TOKEN, anEducationText)

    # schoolName
    # print(edu.schoolName)

    # degreeName
    edu.degreeName = locateData("\r\n" + SECTION_EDUCATION_DEGREE_NAME_TOKEN + "(.*)", anEducationText)
    # print(edu.degreeName)

    date = locateData("Dates attended or expected graduation (.*) –", anEducationText)
    if date is None:
        edu.startDateYYYY = ""

    date = locateData("Dates attended or expected graduation [0-9]{4} – (.*)", anEducationText)
    if date is None:
        edu.endDateYYYY = ""
    # print(edu.endDateYYYY)

    return edu


def locateData(pattern, anExperience, flags=0):
    # p = re.compile("\r\nLocation(.*)See [less|more]", re.DOTALL)
    p = re.compile(pattern, flags)

    match = p.search(anExperience)
    if (match is not None):
        return match.group(1)
    else:
        return None


def loadData(fileName):
    db = resumeDB_pb2.ResumeDB()
    try:
        f = open(fileName, "rb")
        db.ParseFromString(f.read())
        f.close()
    except IOError:
        print("cannot load data from " + fileName)

    return db


def saveData(fileName, db):
    f = open(fileName, "wb")
    f.write(db.SerializeToString())
    f.close()


if __name__ == '__main__':
    main()
