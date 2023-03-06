import csv
import json
import random
import logging

import npcEnneagramGenerator
import npcPromptGenerator
from npcGPTCall import sendPrompt
from diceRoller import Dice_Roller


class NPC:
    def __init__(self):
        self.NPCName = ""
        self.NPCEducation = ""
        self.NPCSex = ""
        self.NPCSexualOrientation = ""

        self.NPCOccupation = ""
        self.NPCRace = ""
        self.NPCSize = ""
        self.NPCSpeed = ""

        self.eSum = {}

        self.NPCStats = []
        self.NPCLanguages = []
        self.NPCPronouns = []
        self.Enneagram = []

        self.NPCAppearance = {"Height": "",
                              "Weight": "",
                              "Age": "",
                              "Gender": "",
                              "Race": "",
                              "Coverings": "",
                              "Face": "",
                              "Eyes": "",
                              "Body": "",
                              "Clothes": ""}

        self.NPCInformation = {}

        self.NPCPersonality = {"Desire": "",
                               "Fear": "",
                               "MentalState": "",
                               "Motivation": "",
                               "Overview": "",
                               "WorldView": "",
                               "SelfView": "",
                               "Interactions": None}

        self.NPCPersonalBackground = {"Occupation": "",
                                      "Friends": [],
                                      "Siblings": [],
                                      "Relatives": [],
                                      "Partners": [],
                                      "RomanticInterests": [],
                                      "DefiningEvents": [],
                                      "RecentEvents": []}

        self.NPCFamilyBackground = {"Reputation": "",
                                    "Bond": "",
                                    "Wealth": "",
                                    "DefiningEvents": [],
                                    "RecentEvents": []}

        self.NPCBackground = {"PersonalBackground": self.NPCPersonalBackground,
                              "FamilyBackground": self.NPCFamilyBackground}

        self.NPCData = {"Appearance": self.NPCAppearance,
                        "Information": self.NPCInformation,
                        "Personality": self.NPCPersonality,
                        "Background": [self.NPCPersonalBackground,
                                       self.NPCFamilyBackground]}

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

    def generateBodyType(self, height, weight):
        bodyType = ""
        bodyID = 0

        meters = height / 100
        BMI = round((weight / meters**2), 2)

        # Selects a level of health for how the person treats their body
        # 1 = In shape, 2 = Average, 3 = Not in shape
        healthLevel = random.randint(1, 3)

        if BMI <= 18.5:
            bodyID = 0
        elif 18.5 < BMI <= 24.9:
            bodyID = 1
        elif 25 < BMI <= 29.29:
            bodyID = 2
        else:
            bodyID = 3

        match healthLevel:
            case 1:
                if bodyID == 0:
                    bodyType = "Sinewy"
                elif bodyID == 1:
                    bodyType = "Lean"
                elif bodyID == 2:
                    bodyType = "Buff"
                else:
                    bodyType = "Massive"
            case 2:
                if bodyID == 0:
                    bodyType = "Thin"
                elif bodyID == 1:
                    bodyType = "Average"
                elif bodyID == 2:
                    bodyType = "Slightly Larger"
                else:
                    bodyType = "Larger"
            case 3:
                if bodyID == 0:
                    bodyType = "Reedy"
                elif bodyID == 1:
                    bodyType = "Soft"
                elif bodyID == 2:
                    bodyType = "Plump"
                else:
                    bodyType = "Fat"

        return bodyType

    def generateAppearance(self):
        ft, inch, lbs = 0, 0, 0

        if self.NPCSize == "Medium":
            ft = random.randint(4, 7)
            inch = random.randint(0, 11)
            lbs = random.randint(110, 250)
        else:
            ft = random.randint(2, 3)
            inch = random.randint(0, 11)
            lbs = random.randint(75, 110)

        inches = (ft * 12) + inch

        cm = self.imperialToMetric(inches, 0)
        self.NPCAppearance.update({"Height": f"{ft}ft {inch}in / {cm}cm"})

        kg = self.imperialToMetric(lbs, 1)
        self.NPCAppearance.update({"Weight": f"{lbs}lbs / {kg}kg"})

        bodyType = self.generateBodyType(cm, kg)
        self.NPCAppearance.update({"Body": f"{bodyType}"})

        return

    def baseInfoParse(self, baseInfo):
        statName = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
        firstLevelStats, buffs = [], []

        for h, i in enumerate(baseInfo):
            match h:
                case 0:
                    self.NPCOccupation = i["Name"]

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
                    self.NPCRace = f"{subRace} {race}"

                    ageMin = i["Adult_Age_Min"]
                    ageMax = i["Adult_Age_Max"]
                    age = random.randint(int(ageMin), int(ageMax))
                    self.NPCAppearance.update({"Age": f"{age}"})

                    self.NPCSize = i["Size"]
                    self.NPCSpeed = i["Speed"]

                    self.generateAppearance()

                    languages = i["Language"]
                    self.NPCLanguages = languages.split(", ")

                    firstLevelStats = Dice_Roller().roll_ndx_y_times(4, 6, 7, True)
                    for stat in statName:
                        buffs.append(i[f"{stat}"])
                    self.getStats(buffs, firstLevelStats)
                case 2:
                    self.NPCAppearance.update({"Gender": i["Gender"]})
                    self.NPCPronouns.extend((i["Pronouns"],
                                             i["Secondary_Pronouns"],
                                             i["Tirtiary_Pronouns"]))
                case 3:
                    self.NPCSexualOrientation = i["Sexual_Orientation"]

        return jobStatus, ownership

    def addEnneagramData(self, NPCEnneagram):
        self.NPCInformation.update({"Alignment": NPCEnneagram.alignment})
        self.NPCInformation.update(
            {"AlignmentIdeology": NPCEnneagram.subAlignment})
        self.NPCInformation.update({"Stress": NPCEnneagram.baseStress})
        self.NPCInformation.update(
            {"StressThreashold": NPCEnneagram.stressThreashold})

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

    def buildPromptData(self, iteration):
        if iteration == 1:
            promptData = str(self.eSum) + \
                str(self.NPCPersonality.get("MentalState"))
        elif iteration == 2:
            promptData = self.NPCPersonality.get(
                "Overview") + self.NPCPersonality.get("MentalState")

        return promptData

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
        # also determines if the NPC can own a business
        self.sexSelector()
        jobStatus, ownership = self.baseInfoParse(baseInfo)

        # Generates name and education

        # Generates and derives personality data for prompt loading
        NPCEnneagram = npcEnneagramGenerator.npcEnneagramGenerator()
        NPCEnneagram.generateInfo()

        #  --Updates the NPCInformation list with information from the generateInfo() function
        self.initialUpdate()

        self.NPCInformation.update({"Alignment": NPCEnneagram.alignment})
        self.NPCInformation.update(
            {"AlignmentIdeology": NPCEnneagram.subAlignment})
        self.NPCInformation.update({"Stress": NPCEnneagram.baseStress})
        self.NPCInformation.update(
            {"StressThreashold": NPCEnneagram.stressThreashold})

        #  --Compiles Enneagram data into NPC public var, which is used as initial prompt data
        preProcEnneagram = NPCEnneagram.enneagramData
        for count, data in enumerate(preProcEnneagram):
            procEnneagram = self.processEnneagramData(
                data, NPCEnneagram.LOD[count])
            procEnneagramList.append(procEnneagram)
        mentalState.update({"mixPercentage": NPCEnneagram.dataBlendOut})
        procEnneagramList.append(mentalState)
        self.Enneagram = procEnneagramList

        # generate personal(past experiences and relationships) background and family background

        # derive skills and abilities from occupation and background

        # generate speech patterns and quirks

        # API to edit generated character

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

    def imperialToMetric(imperial, mode):
        # Converts input imperial to metric based on mode
        # Mode 0 is inches to cm
        # Mode 1 is lbs to kg

        metric = 0
        match mode:
            case 0:
                metric = imperial * 2.54
            case 1:
                metric = imperial * 0.453592

        return metric
