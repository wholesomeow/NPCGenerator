import logging


class npcDetailGenerator:
    def __init__(self, promptFileCompile, promptFileCreate_1, promptFileCreate_2):
        self.promptFileCompile = promptFileCompile
        self.promptFileCreate_1 = promptFileCreate_1
        self.promptFileCreate_2 = promptFileCreate_2
        self.npcPromptData = []
        self.npcDataCreate_1 = []
        self.npcDataCreate_2 = []
        self.npcStoredData = []

        self.npcPromptOut = ""
        self.npcPromptOut_1 = ""
        self.npcPromptOut_2 = ""
        self.promptOutFileName = 0
        self.promptResponse = {}

    def storeData(self, response):
        for l in response:
            if len(l) > 0:
                self.npcStoredData.append(l)

        return

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
        percentages = npcDetail[27]

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

    def dataToPromptCompile(self):
        with open(f"{self.promptFileCompile}", "r") as f:
            npcPromptCompile = f.read()

        self.npcPromptOut = npcPromptCompile + str(self.npcPromptData)

        return

    def gatherResponse_1(self, s):
        result_1 = []
        varList = ["ESum1", "ESum2", "ESum3", "MentalSum"]
        for char in s.splitlines():
            if ":" in char:
                start_index = 0
                end_index = char.index(":")
                substring = char[start_index:end_index].strip()
                if substring in varList:
                    result_1.append(char)

        return result_1

    def gatherResponse_2(self, s):
        result_2 = []
        varList = ["Overview", "MentalSum"]
        for char in s.splitlines():
            if ":" in char:
                start_index = 0
                end_index = char.index(":")
                substring = char[start_index:end_index].strip()
                if substring in varList:
                    result_2.append(char)

        return result_2

    def dataToPrompCreate_1(self):
        i = 0
        with open(f"{self.promptFileCreate_1}", "r") as f:
            npcPromptCreate_1 = f.read()

        self.npcPromptOut_1 = npcPromptCreate_1 + str(self.npcDataCreate_1)

        return

    def dataToPrompCreate_2(self):
        i = 0
        with open(f"{self.promptFileCreate_2}", "r") as f:
            npcPromptCreate_2 = f.read()

        self.npcPromptOut_2 = npcPromptCreate_2 + str(self.npcDataCreate_2)

        return

    def generatePromptCompile(self, npcDetail):
        self.cycleDetail(npcDetail)
        self.dataToPromptCompile()

        return

    def generatePromptCreate_1(self, responseCompile):
        for a in responseCompile:
            self.npcDataCreate_1.append(a)
        self.dataToPrompCreate_1()

        return

    def generatePromptCreate_2(self, responseCreate_1):
        for b in responseCreate_1:
            if len(b) > 0:
                self.npcDataCreate_2.append(b)
        self.dataToPrompCreate_2()

        return

    def testFile(self, npcDetail):
        self.cycleDetail(npcDetail)
        print(self.npcPromptData)

        return
