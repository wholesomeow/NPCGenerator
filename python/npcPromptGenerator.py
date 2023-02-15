import random
import logging


class npcDetailGenerator:
    def __init__(self, promptFile):
        self.promptFile = promptFile
        self.npcPromptData = []

        self.npcPrompt = ""
        self.promptOutFileName = 0
        self.promptResponse = {}

    def detailToData(self, npcDetail, i):
        promptNamesCounter = 0
        varDict = {}
        dataDetail, LOD = [], []
        keyWords = ["briefDesc", "basicFear", "basicDesire", "keyMotivations"]
        promptVarNames = ["npc_MixPercentage", "npc_Description", "npc_Fear", "npc_Desire", "npc_Motivations",
                          "npc_MentalState"]

        dataDetail = npcDetail[24]
        detail = dataDetail[i]
        LOD = npcDetail[28]
        numLOD = LOD[i]
        percentages = npcDetail[26]

        varDict.update(
            {promptVarNames[promptNamesCounter]: percentages[i]})
        promptNamesCounter += 1

        # Collect needed data from the generated NPC json file for the Dominant Type
        for keyword in keyWords:
            varDict.update(
                {promptVarNames[promptNamesCounter]: detail.get(keyword)})
            promptNamesCounter += 1

        # Get Dominant Level of Development and remove the number at the start of the string to use for the Wing Level of Development
        currentLOD = detail.get("levelOfDevelopment")
        varDict.update(
            {promptVarNames[promptNamesCounter]: currentLOD[numLOD - 1]})
        promptNamesCounter += 1

        return varDict

    def cycleDetail(self, npcDetail):
        for i in range(3):
            varDict = self.detailToData(npcDetail, i)
            self.npcPromptData.append(varDict)

        return

    def dataToPrompt(self):
        self.promptOutFileName = random.randint(10000, 19999)

        with open(f"{self.promptFile}", "r") as f:
            npcPrompt = f.read()

        for d in self.npcPromptData:
            self.npcPrompt = npcPrompt + str(d)

        return

    def generatePrompt(self, npcDetail):
        self.cycleDetail(npcDetail)
        self.dataToPrompt()

    def testFile(self, npcDetail):
        self.cycleDetail(npcDetail)
        print(self.npcPromptData)
