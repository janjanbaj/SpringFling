import numpy as np
import bisect
from stable_matching import generate_responses, generate_prefrence_list, flatten_preference_dictionary, stable_matching_github, ppdictionary

NUMBER_OF_PEOPLE = 5
NUMBER_OF_CATEGORIES = 5
NUMBER_OF_QUESTIONS = 10

def random_test_states(m=2):
    print("Statements: ", ['I care about what goes on in campus! ', 'I want to go into the Cadaver tunnels! ', "Streaking the colonnade is cool, I'd do it! ", 'I support the Spectator! '])
    malesRT = generate_responses(NUMBER_OF_PEOPLE = m, NUMBER_OF_CATEGORIES = 1, NUMBER_OF_QUESTIONS = 3)
    femalesRT = generate_responses(NUMBER_OF_PEOPLE = m, NUMBER_OF_CATEGORIES = 1, NUMBER_OF_QUESTIONS = 3)
    valueToQuestion = {1:"Strongly Agree", 2:"Agree", 3:"Neutral", 4:"Disagree", 5:"Strongly Disagree"}
    allMalesRT = []
    for i in range(m):
        maleQualitive=[]
        for j in range(len(malesRT[0][0])):
            maleQualitive.append(valueToQuestion[malesRT[i][0][j]])
        allMalesRT.append(maleQualitive)
    
    allFemalesRT = []
    for l in range(m):
        femaleQualitive=[]
        for s in range(len(femalesRT[0][0])):
            femaleQualitive.append(valueToQuestion[femalesRT[l][0][s]])
        allFemalesRT.append(femaleQualitive)
    
    print("\nMales:\n", allMalesRT, "\n\nFemales:\n", allFemalesRT, "\n")
    
    male_preferenceRT, female_preferenceRT = generate_prefrence_list(malesRT, femalesRT)

    mdRT, fdRT = flatten_preference_dictionary(male_preferenceRT, female_preferenceRT)
    
    print("Male Preferences")
    ppdictionary(mdRT)

    print("\nFemale Preferences")
    ppdictionary(fdRT)

    print()
    
    matches = stable_matching_github(mdRT, fdRT)

    ppdictionary(matches)

    return allMalesRT, allFemalesRT

def controlled_test_states(m=2):
    print("\nPredicted M0 should like F1, M2 should like F0. F0 should like M1 and F1 should like M0\n")
    print("Statements: ", ['I care about what goes on in campus! ', 'I want to go into the Cadaver tunnels! ', "Streaking the colonnade is cool, I'd do it! ", 'I support the Spectator! '])
    malesCT = np.array([[[2, 2, 2, 4]], [[1, 3, 3, 1]]])
    femalesCT = np.array([[[2, 2, 2, 1]], [[1, 2, 3, 5]]])
    valueToQuestion = {1:"Strongly Agree", 2:"Agree", 3:"Neutral", 4:"Disagree", 5:"Strongly Disagree"}
    allMalesCT = []
    for i in range(m):
        maleQualitive=[]
        for j in range(len(malesCT[0][0])):
            maleQualitive.append(valueToQuestion[malesCT[i][0][j]])
        allMalesCT.append(maleQualitive)
    
    allFemalesCT = []
    for l in range(m):
        femaleQualitive=[]
        for s in range(len(femalesCT[0][0])):
            femaleQualitive.append(valueToQuestion[femalesCT[l][0][s]])
        allFemalesCT.append(femaleQualitive)
    
    print("\nMales:\n", allMalesCT, "\n\nFemales:\n", allFemalesCT, "\n")
    
    male_preferenceCT, female_preferenceCT = generate_prefrence_list(malesCT, femalesCT)

    mdCT, fdCT = flatten_preference_dictionary(male_preferenceCT, female_preferenceCT)
    
    print("Male Preferences")
    ppdictionary(mdCT)

    print("\nFemale Preferences")
    ppdictionary(fdCT)

    print()
    
    matches = stable_matching_github(mdCT, fdCT)

    ppdictionary(matches)

    return allMalesCT, allFemalesCT

def take_questionaire(arr=None):
    ans = []
    quals= []
    qualsStatement = []
    
    
    valueToQuestion = {"Strongly Agree":1, "Agree":2, "Neutral":3, "Disagree":4, "Strongly Disagree":5 }
    
    questions = ["I care about what goes on in campus! ", 
                 "I want to go into the Cadaver tunnels! ",
                 "Streaking the colonnade is cool, I'd do it! ",
                 "I support the Spectator! "]
    if arr != None:
        for i in range(len(questions)):
            qual = arr[i]
            while qual not in valueToQuestion:
                print("Error please enter a proper array")
                return [], [], []
            qualsStatement.append("I " + qual + " that " + questions[i])
            ans.append(valueToQuestion[qual])
            quals.append(qual)
        return ans, quals, qualsStatement
    
    print("Please answer: Strongly Agree, Agree, Neutral, Disagree, Strongly Disagree")
    for i in questions:
        qual = input(i)
        while qual not in valueToQuestion:
            print("Please answer: Strongly Agree, Agree, Neutral, Disagree, Strongly Disagree")
            qual = input(i)
        print()
        qualsStatement.append("I " + qual + " that " + i)
        ans.append(valueToQuestion[qual])
        quals.append(qual)

    return ans, quals, qualsStatement

if __name__ == "__main__":
    print("\nQuestionaire------------------------------------------------------------")
    yesNo = input("Would you like to take the questionaire?(y/n) ")
    if yesNo in ["y", "Y", "Yes", "yes"]:
        results, qualResults, qualStatements = take_questionaire()
        # You can also default values into questionaire
        # results, qualResults, qualStatements = take_questionaire(["Agree", "Disagree", "Strongly Disagree", "Strongly Agree"])
        print("You answered: ", qualStatements)
        print("Simply put: ", qualResults)
        print("Here is how they are represented: ", results)
    else:
        print("Skipping Questionaire\n")
    
    input("\n\nPress Enter to see Random Test: ")
    print("\n\nRandom Test States------------------------------------------------------")
    
    males, females = random_test_states()

    input("\n\nPress Enter to see Controlled Test: ")
    print("\n\nControlled Test States---------------------------------------------")
    controlled_test_states()