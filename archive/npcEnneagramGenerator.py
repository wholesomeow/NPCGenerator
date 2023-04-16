import json
import random
import logging

from diceRoller import Dice_Roller

# Generates data from the compiled Enneagram Data and then derives additional NPC data from the selected Enneagram Data


class npcEnneagramGenerator:
    def __init__(self):
        self.npcDetail = []
        self.enneagramData = []
        self.dataBlendOut = []
        self.LOD = []

        self.alignment = ""
        self.subAlignment = ""
        self.centerType = ""
        self.dominantEmotion = ""

        self.baseStress = 0
        self.stressThreashold = 0

        logging.info("npcInfoGenerator Class Initialized")

    def r_DevelopmentLevel(self, EPD):
        # Selects a random Level of Development with bias towards average levels
        # with 1 being healthiest and 9 being unhealthiest
        levelOfDev = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        developmentProb = [0.0015, 0.025, 0.135,
                           0.226, 0.226, 0.226, 0.135, 0.025, 0.0015]
        LODsel = random.choices(levelOfDev, developmentProb)

        return self.LOD.append(LODsel[0])

    def alignmentGenerator(self, max):
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
        elif self.dominantEmotion == "Anger":
            alignmentPrefix = "Chaotic "

        # Gets the LOD from the "Main Type" designated in r_DataBlend
        mainLOD = self.LOD[max]

        # Choose between Good(0), Neutral(1), or Evil(2)
        # Based on Level of Development
        if 1 <= mainLOD <= 3:
            self.alignment = alignmentPrefix + "Good"
        elif 4 <= mainLOD <= 6:
            self.alignment = alignmentPrefix + "Neutral"
        elif 7 <= mainLOD <= 9:
            self.alignment = alignmentPrefix + "Evil"

        # Subalignment Selection
        subNum = random.randint(0, 3)
        match self.alignment:
            case "Lawful Good":
                subAlignment = aEmotions00[subNum]
            case "Lawful Neutral":
                self.subAlignment = aEmotions01[subNum]
            case "Lawful Evil":
                self.subAlignment = aEmotions02[subNum]
            case "Neutral Good":
                self.subAlignment = aEmotions10[subNum]
            case "Neutral Neutral":
                self.subAlignment = aEmotions11[subNum]
            case "Neutral Evil":
                self.subAlignment = aEmotions12[subNum]
            case "Chaotic Good":
                self.subAlignment = aEmotions20[subNum]
            case "Chaotic Neutral":
                self.subAlignment = aEmotions21[subNum]
            case "Chaotic Evil":
                self.subAlignment = aEmotions22[subNum]

        return subNum + 1, mainLOD

    def selectEnneagram(self, input, ranType):
        thinking, feeling, instinctive = [5, 6, 7], [2, 3, 4], [1, 8, 9]
        mainData = input.get("mainData")
        ranType -= 1
        centerTypeNum = ranType + 1

        if centerTypeNum in thinking:
            self.dominantEmotion = "Fear"
            self.centerType = "Thinking"
        elif centerTypeNum in feeling:
            self.dominantEmotion = "Shame"
            self.centerType = "Feeling"
        elif centerTypeNum in instinctive:
            self.dominantEmotion = "Anger"
            self.centerType = "Instinctive"

        return mainData[ranType]

    def stressCalc(self, subNum, mainLOD):
        stress = 10000
        threashold = random.uniform(15.0, 25.0)

        # Takes default stress value and creates a base stress from mental health (Level of Development)
        if mainLOD > 5:
            stress -= 1000 * mainLOD
            self.baseStress = stress
        elif mainLOD < 5:
            stress += 1000 * mainLOD
            self.baseStress = stress

        # Creates a stress threashold based on Alignment Ideology
        # with bonus from mental health
        if subNum <= 2:
            threashold += random.uniform(7.0, 13.0)
        else:
            threashold -= random.uniform(7.0, 13.0)

        threashold += 10.0 - mainLOD * random.uniform(1.0, 10.0)
        self.stressThreashold = float("{:.2f}".format(threashold * 100))

        return

    def r_dataBlend(self):
        # Creates three percentages for the blend of the three selected Enneagram Types. Adds up to 100%
        float1 = random.uniform(0, 100)
        float2 = random.uniform(0, 100 - float1)
        float3 = 100.0 - float1 - float2

        pfloat1 = float("{:.2f}".format(float1))
        pfloat2 = float("{:.2f}".format(float2))
        pfloat3 = float("{:.2f}".format(float3))

        self.dataBlendOut.extend((pfloat1, pfloat2, pfloat3))

        # Finds the largest of the three values and sets that as the "Main Type"
        for e, i in enumerate(self.dataBlendOut):
            current = i
            max = e
            if i > current:
                current = i
                max = e
            else:
                continue

        return max

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
        # Builds Enneagram personality data dict
        with open("json/enneagramDataCompiled.json", "r") as e:
            ennData = json.load(e)

        # Selects three random Enneagram types (with LODs for each) and creates a blend percentage of the three
        # This is where that ugly as hell solution comes into play - bleh
        ranType = 0
        types = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for selection in range(3):
            if selection == 0:
                prevType, ranType = self.pickFirst(ennData, types, ranType)
                self.r_DevelopmentLevel(self.enneagramData)
            elif selection == 1:
                storedType, prevType, ranType = self.pickSecond(
                    ennData, types, prevType, ranType)
                self.r_DevelopmentLevel(self.enneagramData)
            elif selection == 2:
                self.pickThird(ennData, types, storedType,
                               prevType, ranType)
                self.r_DevelopmentLevel(self.enneagramData)
        max = self.r_dataBlend()

        subNum, mainLOD = self.alignmentGenerator(max)
        self.stressCalc(subNum, mainLOD)

        # NOTE: npcDetail has 9 elements (Update as needed)
        self.npcDetail.append(self.alignment)
        self.npcDetail.append(self.subAlignment)
        self.npcDetail.append(self.baseStress)
        self.npcDetail.append(self.stressThreashold)
        self.npcDetail.append(self.enneagramData)
        self.npcDetail.append(self.centerType)
        self.npcDetail.append(self.dominantEmotion)
        self.npcDetail.append(self.dataBlendOut)
        self.npcDetail.append(self.LOD)
