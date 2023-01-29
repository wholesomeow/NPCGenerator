import csv
import json
import random
import logging

from diceRoller import Dice_Roller


class npcInfoGenerator:
    def __init__(self):
        self.npcDetail = []
        self.baseInfo = []

        self.sexID = 100000000000
        self.typeID = 10000000
        self.baseID = 1250000
        self.wingID = 0
        self.subID = 500000
        self.centerID = 0
        self.centerType = ""
        self.alignmentID = 10000
        self.subAlignmentID = 5000

        self.enneagramData = {}
        self.dominantWing = {}
        self.wingBlendOut = 0.00

        self.LOD = 0

        self.alignment = ""
        self.subAlignment = ""
        self.baseStats = []

        self.sex = ""
        self.ageID = 100000
        self.age = 0

        self.jobID = 0
        self.jobCategory = ""
        self.jobName = ""
        self.jobDescription = ""
        self.owner = False
        self.statusLevel = 0

        self.raceID = 0
        self.race = ""
        self.subRace = ""
        self.size = ""
        self.speed = 0
        self.lanuages = ""
        self.raceExtraInfo = ""

        self.genderID = 0
        self.gender = ""
        self.genderDescription = ""
        self.pronouns1 = ""
        self.pronouns2 = ""
        self.pronouns3 = ""

        self.orientationID = 0
        self.orientation = ""
        self.orientationDescription = ""
        logging.info("npcInfoGenerator Class Initialized")

    def sexSelector(self):
        r_sex = random.randint(1, 99)
        if r_sex in range(1, 33):
            self.sex = "Male"
        elif r_sex in range(34, 66):
            self.sex = "Female"
        elif r_sex in range(67, 99):
            self.sex = "Other"

        return

    def loadCSV(self, fileName):
        output = []
        # Import the different csv files and pull random values
        with open(fileName, newline='', encoding='utf8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                output.append(row)

        return output

    def baseInfoPick(self, input):
        # Generate different random values, one for each csv
        randomValue = random.randint(0, len(input) - 1)

        return self.baseInfo.append(input[randomValue])

    def baseInfoParse(self):
        # Parse info from the randomly selected csv data for Job, Gender, Race, and Sexual Orientation
        statusList, statBuffs = [], []
        statusValue = 0

        if self.sex == "Male":
            self.sexID
        elif self.sex == "Female":
            self.sexID *= 2
        elif self.sex == "Other":
            self.sexID *= 3

        for n, i in enumerate(self.baseInfo):
            match n:
                case 0:
                    self.jobID = int(i["ID"])
                    self.jobCategory = i["Category"]
                    if self.sex == "Male":
                        self.jobName = i["Name"]
                    else:
                        self.jobName = i["Alt_Name"]
                    self.jobDescription = i["Description"]
                    own = i["Can_Own"]
                    if int(own) == 0:
                        self.owner = False
                    else:
                        self.owner = True
                    statusMin = i["Min_Status_Level"]
                    statusMax = i["Max_Status_Level"]
                    self.statusLevel = random.randint(
                        int(statusMin), int(statusMax))
                case 1:
                    self.raceID = int(i["ID"])
                    self.race = i["Race"]
                    self.subRace = i["Race"]
                    ageMin = i["Adult_Age_Min"]
                    ageMax = i["Adult_Age_Max"]
                    self.age = random.randint(int(ageMin), int(ageMax))
                    self.ageID *= self.age
                    self.size = i["Size"]
                    self.speed = int(i["Speed"])
                    self.lanuages = i["Language"]
                    statBuffs.extend((i["Str"],
                                     i["Dex"],
                                     i["Con"],
                                     i["Int"],
                                     i["Wis"],
                                     i["Cha"]))
                    self.raceExtraInfo = i["Extra"]
                case 2:
                    self.genderID = int(i["ID"])
                    self.gender = i["Gender"]
                    self.genderDescription = i["Gender_Description"]
                    self.pronouns1 = i["Pronouns"]
                    self.pronouns2 = i["Secondary_Pronouns"]
                    self.pronouns3 = i["Tirtiary_Pronouns"]
                case 3:
                    self.orientationID = int(i["ID"])
                    self.orientation = i["Sexual_Orientation"]
                    self.orientationDescription = i["Sexual_Orientation_Description"]

        return statBuffs

    def r_DevelopmentLevel(self, EPD):
        # Selects a random Level of Development with bias towards average levels
        # with 1 being healthiest and 9 being unhealthiest
        levelOfDev = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        developmentProb = [0.0015, 0.025, 0.135,
                           0.226, 0.226, 0.226, 0.135, 0.025, 0.0015]
        LODsel = random.choices(levelOfDev, developmentProb)
        self.LOD = LODsel[0]

        return self.LOD

    def alignmentGenerator(self):
        alignmentPrefix = ""
        aEmotions00 = ["Collectivism", "Fanaticism",
                       "Individualism", "Relativism"]
        aEmotions01 = ["Parental", "Ascendance", "Community", "Philisophy"]
        aEmotions02 = ["Revolution", "Activism", "Evolutionism", "Conformism"]
        aEmotions10 = ["Literalism", "Free Will", "Progressivim", "Fate"]
        aEmotions11 = ["Judgement", "Passivism", "Intuition", "Pride"]
        aEmotions12 = ["Naturalism", "Authority", "Anarchy", "Freedom"]
        aEmotions20 = ["Systems", "Idealism", "Brutality", "Indulgence"]
        aEmotions21 = ["Corruption", "Certainty", "Destruction", "Uncertainty"]
        aEmotions22 = ["Planning", "Gluttony", "Spontaneity", "Greed"]

        # Alignment Selection
        # Choose between Lawful(0), Neutral(1), Chaotic(2)
        # Based on Enneagram Center Type/Dominant Emotion
        if self.dominantEmotion == "Fear":
            alignmentPrefix = "Lawful "
        elif self.dominantEmotion == "Shame":
            alignmentPrefix = "Neutral "
            self.alignmentID *= 2
        elif self.dominantEmotion == "Anger":
            alignmentPrefix = "Chaotic "
            self.alignmentID *= 3

        # Choose between Good(0), Neutral(1), or Evil(2)
        # Based on Level of Development
        if 1 <= self.LOD <= 3:
            self.alignment = alignmentPrefix + "Good"
        elif 4 <= self.LOD <= 6:
            self.alignment = alignmentPrefix + "Neutral"
            self.alignmentID -= self.subAlignmentID
        elif 7 <= self.LOD <= 9:
            self.alignment = alignmentPrefix + "Evil"
            self.alignmentID += self.subAlignmentID

        # Subalignment Selection
        subNum = random.randint(0, 3)
        match self.alignment:
            case "Lawful Good":
                subAlignment = aEmotions00[subNum]
            case "Lawful Neutral":
                self.subAlignment = aEmotions01[subNum]
                self.subAlignmentID += 125
            case "Lawful Evil":
                self.subAlignment = aEmotions02[subNum]
                self.subAlignmentID += 150
            case "Neutral Good":
                self.subAlignment = aEmotions10[subNum]
                self.subAlignmentID += 175
            case "Neutral Neutral":
                self.subAlignment = aEmotions11[subNum]
                self.subAlignmentID += 200
            case "Neutral Evil":
                self.subAlignment = aEmotions12[subNum]
                self.subAlignmentID += 225
            case "Chaotic Good":
                self.subAlignment = aEmotions20[subNum]
                self.subAlignmentID += 250
            case "Chaotic Neutral":
                self.subAlignment = aEmotions21[subNum]
                self.subAlignmentID += 275
            case "Chaotic Evil":
                self.subAlignment = aEmotions22[subNum]
                self.subAlignmentID += 300

        return

    def r_wingBlend(self):
        output = 0.0
        output = random.uniform(0.0, 0.5)
        output *= 100
        self.wingBlendOut = float("{:.2f}".format(output))

        return

    def wingSelection(self, ennData):
        output = {}

        # Select one of the two wings
        wingVal = self.enneagramData.get("wings")
        ranWing = random.randint(0, 1)
        wing = wingVal[ranWing]

        # Find that wings data and return it
        mainData = ennData.get("mainData")
        output = mainData[wing - 1]

        self.wingID = self.mainTypeID / 2

        return output

    def selectEnneagram(self, input):
        output = {}
        thinking, feeling, instinctive = [5, 6, 7], [2, 3, 4], [1, 8, 9]
        mainData = input.get("mainData")
        ranType = random.randint(0, 8)
        centerTypeNum = ranType + 1

        if centerTypeNum in thinking:
            self.mainTypeID = self.typeID * centerTypeNum
            self.dominantEmotion = "Fear"
            self.centerType = "Thinking Center"
            self.subID *= 1
            self.centerID = self.baseID + self.subID
        elif centerTypeNum in feeling:
            self.mainTypeID = self.typeID * centerTypeNum
            self.dominantEmotion = "Shame"
            self.centerType = "Feeling Center"
            self.subID *= 2
            self.centerID = self.baseID + self.subID
        elif centerTypeNum in instinctive:
            self.mainTypeID = self.typeID * centerTypeNum
            self.dominantEmotion = "Anger"
            self.centerType = "Instinctive Center"
            self.subID *= 3
            self.centerID = self.baseID + self.subID

        # Having the placement of data happen after the ID is created and output is updated
        output = mainData[ranType]

        return output

    def getStats(self, statBuffs):
        statBuffInt = []
        firstLevelStats = Dice_Roller().roll_ndx_y_times(4, 6, 7, True)
        for raceStat in statBuffs:
            statBuffInt.append(int(raceStat))
        for statNum, stat in enumerate(firstLevelStats):
            currentStat = stat + statBuffInt[statNum]
            self.baseStats.append(currentStat)

        return

    def compileID(self):
        num = 0
        IDList = []
        # Add all the class ID values
        IDList.extend((self.sexID,
                       self.typeID,
                       self.baseID,
                       int(self.wingID),
                       self.subID,
                       self.centerID,
                       self.alignmentID,
                       self.subAlignmentID,
                       self.LOD,
                       self.jobID,
                       self.statusLevel,
                       self.raceID,
                       self.genderID,
                       self.orientationID))

        for id in IDList:
            num += id

        # Shameless copied from StackOverflow - forgot to add link and I can't remember where I found it
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if num == 0:
            return alphabet[0]
        arr = []
        arr_append = arr.append  # Extract bound-method for faster access.
        _divmod = divmod  # Access to locals is faster.
        base = len(alphabet)
        while num:
            num, rem = _divmod(num, base)
            arr_append(alphabet[rem])
        arr.reverse()

        return ''.join(arr)

    def generateInfo(self):
        fileList = ["csv/NPC_Job_List.csv", "csv/Races.csv",
                    "csv/Genders.csv", "csv/Sexual_Orientations.csv"]

        # Load and read non-personality data from csv files
        self.sexSelector()
        for fileName in fileList:
            csvOuput = self.loadCSV(fileName)
            self.baseInfoPick(csvOuput)
        statBuffs = self.baseInfoParse()

        # Builds Enneagram personality data dict
        with open("json/enneagramDataCompiled.json", "r") as e:
            ennData = json.load(e)

        self.enneagramData = self.selectEnneagram(ennData)
        self.dominantWing = self.wingSelection(ennData)
        self.r_wingBlend()

        self.getStats(statBuffs)

        self.r_DevelopmentLevel(self.enneagramData)
        self.alignmentGenerator()

        # TODO: Create base stress value, stres threashold, and +/- stress from Level of Development

        # NOTE: npcDetail has 28 elements (Update as needed)
        self.npcDetail.append(self.alignment)
        self.npcDetail.append(self.subAlignment)
        self.npcDetail.append(self.baseStats)
        self.npcDetail.append(self.sex)
        self.npcDetail.append(self.jobCategory)
        self.npcDetail.append(self.jobName)
        self.npcDetail.append(self.jobDescription)
        self.npcDetail.append(self.owner)
        self.npcDetail.append(self.statusLevel)
        self.npcDetail.append(self.race)
        self.npcDetail.append(self.subRace)
        self.npcDetail.append(self.size)
        self.npcDetail.append(self.speed)
        self.npcDetail.append(self.lanuages)
        self.npcDetail.append(self.raceExtraInfo)
        self.npcDetail.append(self.gender)
        self.npcDetail.append(self.genderDescription)
        self.npcDetail.append(self.pronouns1)
        self.npcDetail.append(self.pronouns2)
        self.npcDetail.append(self.pronouns3)
        self.npcDetail.append(self.orientation)
        self.npcDetail.append(self.orientationDescription)
        self.npcDetail.append(self.enneagramData)
        self.npcDetail.append(self.centerType)
        self.npcDetail.append(self.dominantEmotion)
        self.npcDetail.append(self.dominantWing)
        self.npcDetail.append(self.wingBlendOut)
        self.npcDetail.append(self.LOD)

        self.npcID = self.compileID()
        logging.info("NPC Information generated successfully")
