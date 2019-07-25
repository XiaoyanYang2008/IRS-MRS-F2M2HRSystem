import pickle
import re

SECTION_EXPERIENCE_TOKEN = "Experience\r\n"
SECTION_EXPERIENCE_COMPANY_NAME_TOKEN = "Company Name"


def main():
    experienceText = pickle.load(open('experience.pickle', 'rb'))
    # print(experienceText)

    extractExperiences(experienceText)


def extractExperiences(experience):
    records = experience.split('\r\n\r\n')
    cnRecords = experience.split(SECTION_EXPERIENCE_COMPANY_NAME_TOKEN)

    # TODO do UI check when extra empty lines more then company? 8 vs 8 in this case.
    print("length by 1 emptyline %s, by cn %s" % (len(records), len(cnRecords)))

    if (not records[0].startswith(SECTION_EXPERIENCE_TOKEN)):
        return

    # for e in records:
    #     extractAnExperienceData(e)
    extractAnExperienceData(records[0])

    # print(records)


# TODO done regex. Try to build domain class for structure data.
def extractAnExperienceData(anExperience):
    if (anExperience.startswith(SECTION_EXPERIENCE_TOKEN)):
        anExperience = anExperience.replace(SECTION_EXPERIENCE_TOKEN, "")

    # sections = anExperience.split("\r\n")

    # Title
    print(re.search("\r\n(.*)\r\nCompany Name", anExperience).group(1))

    # Titles for multiple titles within a company.
    # print(re.search("\r\nTitle(.*)\r\n", anExperience).group(1))

    # Company
    print(re.search("\r\nCompany Name(.*)\r\n", anExperience).group(1))

    # Dates Employed
    print(re.search("\r\nDates Employed(.*)\r\n", anExperience).group(1))

    # Employment Duration
    print(re.search("\r\nEmployment Duration(.*)\r\n", anExperience).group(1))

    # Location search
    location = re.search("\r\nLocation(.*)\r\n", anExperience).group(1)
    print(location)

    # experienceText
    p = re.compile("\r\nLocation(.*)See [less|more]", re.DOTALL)
    print(p.search(anExperience).group(1))

    return


if __name__ == '__main__':
    main()
