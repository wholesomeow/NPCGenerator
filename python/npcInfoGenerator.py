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
        self.subID = 500000
        self.centerID = 0
        self.centerType = ""
        self.alignmentID = 10000
        self.subAlignmentID = 5000
        self.stressID = 1000

        self.enneagramData = []
        self.dataBlendOut = []

        self.LOD = 0

        self.alignment = ""
        self.subAlignment = ""
        self.baseStats = []

        self.baseStress = 0
        self.stressThreashold = 0

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
                    if self.sex == "Male" or "Other":
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

        # Chooses a personal ideology that the individual follows, either consiously or not
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

        return subNum + 1

    def selectEnneagram(self, input, ranType):
        thinking, feeling, instinctive = [5, 6, 7], [2, 3, 4], [1, 8, 9]
        mainData = input.get("mainData")
        ranType -= 1
        centerTypeNum = ranType + 1

        if centerTypeNum in thinking:
            self.baseID = self.typeID * centerTypeNum
            self.dominantEmotion = "Fear"
            self.centerType = "Thinking Center"
            self.subID *= 1
            self.centerID = self.baseID + self.subID
        elif centerTypeNum in feeling:
            self.baseID = self.typeID * centerTypeNum
            self.dominantEmotion = "Shame"
            self.centerType = "Feeling Center"
            self.subID *= 2
            self.centerID = self.baseID + self.subID
        elif centerTypeNum in instinctive:
            self.baseID = self.typeID * centerTypeNum
            self.dominantEmotion = "Anger"
            self.centerType = "Instinctive Center"
            self.subID *= 3
            self.centerID = self.baseID + self.subID

        # Having the placement of data happen after the ID is created and output is updated
        return mainData[ranType]

    def stressCalc(self, subNum):
        stress = 10000
        threashold = random.uniform(15.0, 25.0)

        # Takes default stress value and creates a base stress from mental health (Level of Development)
        if self.LOD > 5:
            stress -= 1000 * self.LOD
            self.baseStress = stress
        elif self.LOD < 5:
            stress += 1000 * self.LOD
            self.baseStress = stress

        # Creates a stress threashold based on Alignment Ideology
        # with bonus from mental health
        if subNum <= 2:
            threashold += random.uniform(7.0, 13.0)
        else:
            threashold -= random.uniform(7.0, 13.0)

        threashold += 10.0 - self.LOD * random.uniform(1.0, 10.0)
        self.stressThreashold = float("{:.2f}".format(threashold * 100))
        self.stressID += self.baseStress

        return

    def r_dataBlend(self):
        float1 = random.uniform(0, 100)
        float2 = random.uniform(0, 100 - float1)
        float3 = 100.0 - float1 - float2

        pfloat1 = float("{:.2f}".format(float1))
        pfloat2 = float("{:.2f}".format(float2))
        pfloat3 = float("{:.2f}".format(float3))

        self.dataBlendOut.extend((pfloat1, pfloat2, pfloat3))

        return

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
                       self.subID,
                       self.centerID,
                       self.alignmentID,
                       self.subAlignmentID,
                       self.LOD,
                       self.jobID,
                       self.statusLevel,
                       self.raceID,
                       self.genderID,
                       self.orientationID,
                       self.stressID))

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

# This is ugly as hell; gotta figure out a better way
    def pickFirst(self, ennData, types, ranType):
        ranType = random.choice(types)
        prevType = ranType
        self.enneagramData.append(self.selectEnneagram(ennData, ranType))

        return prevType, ranType

    def pickSecond(self, ennData, types, prevType, ranType):
        ranType = random.choice(types)
        if ranType is not prevType:
            self.enneagramData.append(self.selectEnneagram(ennData, ranType))
        else:
            print("Match found... reselecting second")
            ranType = random.choice(types)

        storedType = prevType
        prevType = ranType

        return storedType, prevType, ranType

    def pickThird(self, ennData, types, storedType, prevType, ranType):
        ranType = random.choice(types)
        if ranType is not prevType or storedType:
            self.enneagramData.append(self.selectEnneagram(ennData, ranType))
        else:
            print("Match found... reselecting third")
            ranType = random.choice(types)

        return
# --------------------------------------------------

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

        # Selects three random Enneagram types and creates a blend percentage of the three
        # This is where that ugly as hell solution comes into play - bleh
        ranType = 0
        types = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for selection in range(3):
            if selection == 0:
                prevType, ranType = self.pickFirst(ennData, types, ranType)
            elif selection == 1:
                storedType, prevType, ranType = self.pickSecond(
                    ennData, types, prevType, ranType)
            elif selection == 2:
                self.pickThird(ennData, types, storedType, prevType, ranType)
        self.r_dataBlend()

        self.getStats(statBuffs)

        self.r_DevelopmentLevel(self.enneagramData)
        subNum = self.alignmentGenerator()
        self.stressCalc(subNum)

        # TODO: Create base stress value, stres threashold, and +/- stress from Level of Development

        # NOTE: npcDetail has 30 elements (Update as needed)
        self.npcDetail.append(self.alignment)
        self.npcDetail.append(self.subAlignment)
        self.npcDetail.append(self.baseStats)
        self.npcDetail.append(self.baseStress)
        self.npcDetail.append(self.stressThreashold)
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
        self.npcDetail.append(self.dataBlendOut)
        self.npcDetail.append(self.LOD)

        self.npcID = self.compileID()
        logging.info("NPC Information generated successfully")

    def npcPrintInfo(self):
        printInfo = {}

        printInfo.update({"Alignment": self.alignment})
        printInfo.update({"AlignmentIdeology": self.subAlignment})
        printInfo.update({"Stats": self.baseStats})
        printInfo.update({"JobName": self.jobName})
        printInfo.update({"JobDescription": self.jobDescription})
        printInfo.update({"Race": f"{self.subRace} {self.race}"})
        printInfo.update({"Size": self.size})
        printInfo.update({"Speed": self.speed})
        printInfo.update({"Languages": self.lanuages})
        printInfo.update({"Gender": self.gender})
        printInfo.update({"Sex": self.sex})
        printInfo.update({"Stress": self.baseStress})
        printInfo.update({"StressThreashold": self.stressThreashold})
        printInfo.update({"Pronouns-1": self.pronouns1})
        printInfo.update({"Pronouns-2": self.pronouns2})
        printInfo.update({"Pronouns-3": self.pronouns3})
        printInfo.update({"SexualOrientation": self.orientation})

        return printInfo
