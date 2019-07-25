import pickle


def main():
    experienceText = pickle.load(open('experience.pickle', 'rb'))
    print(experienceText)

    extractExperiences(experienceText)


def extractExperiences(experience):
    records = experience.split('\r\n\r\n')
    # if (records[0] != "Experience\r\n"):
    #     return

    for e in records:
        extractAnExperienceData(e)

    print(records)

#TODO implement this. likely return a domain class as well for ease of structure data.
def extractAnExperienceData():
    return

if __name__ == '__main__':
    main()
