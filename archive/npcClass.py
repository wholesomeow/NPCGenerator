import csv
import json
import random
import logging
from typing import cast

import npcEnneagramGenerator
import npcPromptGenerator
import npcAppearance
from npcGPTCall import sendPrompt
from diceRoller import Dice_Roller


class NPC:
    def __init__(self):
        self.NPCName = "Default"
        self.NPCEducation = "Default"
        self.NPCSex = "Default"
        self.NPCSexualOrientation = "Default"

        self.NPCOccupation = "Default"
        self.NPCRace = "Default"
        self.NPCSize = "Default"
        self.NPCSpeed = "Default"

        self.NPCAppearance = {}

        self.NPCSelfEsteem = 0
        self.stress = 0
        self.stressThresh = 0

        self.eSum = {}

        self.NPCStats = []
        self.NPCLanguages = []
        self.NPCPronouns = []
        self.Enneagram = []

        self.NPCInformation = {}

        self.NPCPersonality = {"Desire": "Default",
                               "Fear": "Default",
                               "MentalState": "Default",
                               "Motivation": "Default",
                               "Overview": "Default",
                               "WorldView": "Default",
                               "SelfView": "Default",
                               "Interactions": None}

        self.NPCPersonalBackground = {"Occupation": "Default",
                                      "Friends": [],
                                      "Siblings": [],
                                      "Relatives": [],
                                      "Partners": [],
                                      "RomanticInterests": [],
                                      "DefiningEvents": [],
                                      "RecentEvents": []}

        self.NPCFamilyBackground = {"Reputation": "Default",
                                    "Bond": "Default",
                                    "Wealth": "Default",
                                    "DefiningEvents": [],
                                    "RecentEvents": []}

        self.NPCBackground = {"PersonalBackground": self.NPCPersonalBackground,
                              "FamilyBackground": self.NPCFamilyBackground}

    def loadCSV(self, fileName):
        csvOutput = []
        with open(fileName, newline='', encoding='utf8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                csvOutput.append(row)

        return csvOutput

    # Generate different random values, one for each csv, and select data from it
    def baseInfoPick(self, csvOuput, baseInfo):
        randomValue = random.randint(0, len(csvOuput) - 1)

        return baseInfo.append(csvOuput[randomValue])

    def sexSelector(self):
        r_sex = random.randint(1, 99)
        if r_sex in range(1, 33):
            self.NPCSex = "Male"
        elif r_sex in range(34, 66):
            self.NPCSex = "Female"
        elif r_sex in range(67, 99):
            self.NPCSex = "Other"

        return

    def getStats(self, buffs, firstLevelStats):
        for index, stat in enumerate(firstLevelStats):
            finalStat = stat + int(buffs[index])
            self.NPCStats.append(finalStat)

        return

    def initSelfEsteem(self, faceValue, jobStatus, ownership):
        return

    # TODO: This
    # This function gets current event, determines how stressful that is to the NPC, and recalcs stress level
    # If post-event, then intakes new stress value from getSelfEsteem and recalcs stress level
    # As stress gets closer to stressThresh, the higher the chance of a mental break
    def getStress(self, mode):
        match mode:
            case "preEvent":
                pass
            case "postEvent":
                pass
        return

    # TODO: and this
    # This function creates a new event object and compares available options to npc personality type to select a probable outcome
    def eventChoice(self):
        npcEventChoice = ""
        return npcEventChoice

    # TODO: and this
    # This function gets decision made from last event and compares that to selfImage (Direction of Integration/Disintegration)
    # If these values don't align, selfEsteem is lowered and stress is increased or vice-versa
    def getSelfEsteem(self, npcEventChoice):
        stressAdd = 0
        return stressAdd

    def baseInfoParse(self, baseInfo):
        statName = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
        firstLevelStats, buffs, coveringlist = [], [], []
        preAppearList = []
        faceTotal = {}
        jobStatus = 0
        ownership = False

        for h, i in enumerate(baseInfo):
            match h:
                case 0:
                    self.NPCOccupation = i["Name"]
                    self.NPCPersonalBackground.update(
                        {"Occupation": self.NPCOccupation})

                    if i["Can_Own"] == 0:
                        ownership = False
                    else:
                        ownership = True

                    statusMin = i["Min_Status_Level"]
                    statusMax = i["Max_Status_Level"]
                    jobStatus = random.randint(
                        int(statusMin), int(statusMax))
                case 1:
                    race = i["Race"]
                    subRace = i["Subrace"]
                    if subRace == "none":
                        self.NPCRace = race
                    else:
                        self.NPCRace = f"{subRace} {race}"
                    preAppearList.append(self.NPCRace)

                    ageMin = i["Adult_Age_Min"]
                    ageMax = i["Adult_Age_Max"]
                    age = random.randint(int(ageMin), int(ageMax))
                    preAppearList.append(age)

                    covering = i["Covering"]
                    covering_Alt = i["Covering_Alt"]
                    coveringlist.append(covering)
                    if covering_Alt == "None":
                        covering_Alt = None
                    else:
                        coveringlist.append(covering_Alt)
                    preAppearList.append(coveringlist)

                    self.NPCSize = i["Size"]
                    preAppearList.append(self.NPCSize)
                    self.NPCSpeed = i["Speed"]

                    languages = i["Language"]
                    self.NPCLanguages = languages.split(", ")

                    firstLevelStats = Dice_Roller().roll_ndx_y_times(4, 6, 7, True)
                    for stat in statName:
                        buffs.append(i[f"{stat}"])
                    self.getStats(buffs, firstLevelStats)
                    charisma = self.NPCStats[5]
                    preAppearList.append(charisma)
                case 2:
                    preAppearList.append(i["Gender"])
                    self.NPCPronouns.extend((i["Pronouns"],
                                             i["Secondary_Pronouns"],
                                             i["Tirtiary_Pronouns"]))
                case 3:
                    self.NPCSexualOrientation = i["Sexual_Orientation"]

        NPCAppearance = npcAppearance.npcAppearance(preAppearList)
        NPCAppearance.generateAppearance()
        NPCAppearance.generateClothing(jobStatus)
        self.NPCAppearance = NPCAppearance.appearance

        faceTotal = NPCAppearance.appearance.get("Face")
        faceTotal = cast(dict, faceTotal)
        face = faceTotal.get("Overview")
        faceValue = 25
        match face:
            case "Unattractive":
                faceValue -= 10
            case "Average":
                faceValue = 25
            case "Attractive":
                faceValue += 10
            case "Gorgeous":
                faceValue += 15

        return jobStatus, ownership, faceValue

    def setEducation(self, jobstatus):
        educationStatus = [
            "No or Limited Formal Education",
            "Some Formal Education",
            "Well Educated within Profession",
            "Some additional Education outside Profession",
            "Well educated in a Formal Institution"
        ]

        if jobstatus <= 3:
            self.NPCEducation = educationStatus[0]
        elif jobstatus >= 4 and jobstatus <= 5:
            self.NPCEducation = educationStatus[1]
        elif jobstatus >= 6 and jobstatus <= 7:
            self.NPCEducation = educationStatus[2]
        elif jobstatus >= 8 and jobstatus <= 10:
            self.NPCEducation = educationStatus[3]
        elif jobstatus >= 11 and jobstatus <= 13:
            self.NPCEducation = educationStatus[4]
        else:
            self.NPCEducation = educationStatus[5]

        return

    def addEnneagramData(self, NPCEnneagram):
        self.NPCInformation.update({"Alignment": NPCEnneagram.alignment})
        self.NPCInformation.update(
            {"AlignmentIdeology": NPCEnneagram.subAlignment})
        self.NPCInformation.update({"Stress": NPCEnneagram.baseStress})
        self.NPCInformation.update(
            {"StressThreashold": NPCEnneagram.stressThreashold})

        self.stress = NPCEnneagram.baseStress
        self.stressThresh = NPCEnneagram.stressThreashold

        return

    def processEnneagramData(self, preProcEnneagram, LOD):
        keyWords = ["briefDesc", "basicFear", "basicDesire", "keyMotivations"]
        procEnneagram = {}

        level = preProcEnneagram.get("levelOfDevelopment"[LOD])

        for word in keyWords:
            procEnneagram.update({f"{word}": preProcEnneagram.get(f"{word}")})

        procEnneagram.update({"mentalState": level})

        return procEnneagram

    # Generates and sends prompts to get final personality data
    def getPromptResponse(self, promptFile, promptData, engine):
        NPCPrompt = npcPromptGenerator.npcPromptGenerator
        generatedPrompt = NPCPrompt.generatePrompt(
            promptFile, str(promptData))
        PromptResponse, PromptUsage = sendPrompt(generatedPrompt, engine)

        return PromptResponse, PromptUsage

    # Generates Prompt Data to be paired with Prompt Text for novel data creation
    # iteration 1 is Prompt 2, iteration 2 is Prompt 3, etc
    def buildPromptData(self, iteration):
        promptData = {}
        if iteration == 1:
            promptData = str(self.eSum) + \
                str(self.NPCPersonality.get("MentalState"))
        elif iteration == 2:
            promptData = self.NPCPersonality.get(
                "Overview") + self.NPCPersonality.get("MentalState")

        return promptData

    # Updates object information with data from first Prompt response
    def updateNPCResponse(self, response, iteration):
        match iteration:
            case 0:
                keyWords, holding, eSum = ["Desire", "Fear",
                                           "MentalState", "Motivation"], [], []

                for string in response:
                    s = string.partition(":")[2]
                    s.strip()
                    holding.append(s)

                i = 0
                while i < 3:
                    eSum.append(holding[0])
                    del holding[0]
                    i += 1

                self.eSum.update({"ESum1": eSum[0]})
                self.eSum.update({"ESum2": eSum[1]})
                self.eSum.update({"ESum3": eSum[2]})

                for count, word in enumerate(keyWords):
                    self.NPCPersonality.update({f"{word}": holding[count]})
            case 1:
                keyWords, holding = ["Overview", "WorldView", "SelfView"], []

                for string in response:
                    s = string.partition(":")[2]
                    s.strip()
                    holding.append(s)

                for count, word in enumerate(keyWords):
                    self.NPCPersonality.update({f"{word}": holding[count]})
            case 2:
                holding = []

                for string in response:
                    s = string.partition(":")[2]
                    s.strip()
                    holding.append(s)

                self.NPCPersonality.update({"Interactions": holding})

        return

    def updateData(self):
        self.NPCData = {"Appearance": self.NPCAppearance,
                        "Information": self.NPCInformation,
                        "Personality": self.NPCPersonality,
                        "Background": [self.NPCPersonalBackground,
                                       self.NPCFamilyBackground]}
        return

    def createNPC(self):
        # Initializes base information list where most non-personality data will be stored until allocation in public variables
        baseInfo, procEnneagramList = [], []
        mentalState = {}

        # Load info from CSV and TXT Files
        CSVFiles = ["csv/NPC_Job_List.csv", "csv/Races.csv",
                    "csv/Genders.csv", "csv/Sexual_Orientations.csv"]
        TXTFiles = ["txt/likesDislikes.txt"]

        for filename in CSVFiles:
            csvOutput = self.loadCSV(filename)
            self.baseInfoPick(csvOutput, baseInfo)

        # Generates Race, Job, Gender, Sex, and base D&D Stats
        # baseInfoParse also generates the NPC Appearance, status level of their job,
        # and if the NPC owns a business
        self.sexSelector()
        jobStatus, ownership, faceValue = self.baseInfoParse(baseInfo)
        self.initSelfEsteem(jobStatus, ownership, faceValue)

        # Generates name and education
        self.setEducation(jobStatus)

        # Generates and derives personality data for prompt loading
        NPCEnneagram = npcEnneagramGenerator.npcEnneagramGenerator()
        NPCEnneagram.generateInfo()

        #  --Updates the NPCInformation list with information from the generateInfo() function
        self.initialUpdate()
        self.addEnneagramData(NPCEnneagram)

        #  --Compiles Enneagram data into NPC public var, which is used as initial prompt data
        preProcEnneagram = NPCEnneagram.enneagramData
        for count, data in enumerate(preProcEnneagram):
            procEnneagram = self.processEnneagramData(
                data, NPCEnneagram.LOD[count])
            procEnneagramList.append(procEnneagram)
        mentalState.update({"mixPercentage": NPCEnneagram.dataBlendOut})
        procEnneagramList.append(mentalState)
        self.Enneagram = procEnneagramList

        # derive skills and abilities from occupation and background

        # generate personal(past experiences and relationships) background and family background
        # NOTE: For experiences gen, loop through eventSelect -> getStress -> eventChoice -> getSelfEsteem -> getStress

        # generate speech patterns and quirks

        # API to edit generated character

        self.updateData()

    def initialUpdate(self):
        keyWords = ["Name", "Education", "Sex", "SexualOrientation",
                    "Race", "Size", "Speed", "Stats", "Languages", "Pronouns"]
        var = [self.NPCName, self.NPCEducation, self.NPCSex, self.NPCSexualOrientation, self.NPCRace,
               self.NPCSize, self.NPCSpeed, self.NPCStats, self.NPCLanguages, self.NPCPronouns]

        for count, item in enumerate(keyWords):
            self.NPCInformation.update({f"{item}": var[count]})

        return

    # Misc Utility Functions
    def printBaseInfo(self, baseInfo):
        print(baseInfo)

        return

    def npcPrintInfo(self):
        return self.NPCData
