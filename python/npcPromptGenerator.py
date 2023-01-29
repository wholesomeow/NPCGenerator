import openai
import random
import logging


class npcDetailGenerator:
    def __init__(self, promptFile):
        self.promptFile = promptFile
        self.npcVarDict = {}

        self.npcPrompt = ""
        self.promptOutFileName = 0
        self.promptResponse = {}

    def detailToData(self, npcDetail):
        promptNamesCounter = 0
        dominantDetail, wingDetail = {}, {}
        keyWords = ["briefDesc", "basicFear", "basicDesire", "keyMotivations"]
        promptVarNames = ["npc_MixPercentage", "npc_DominantDescription", "npc_DominantFear", "npc_DominantDesire", "npc_DominantMotivations",
                          "npc_DominantMentalState", "npc_WingDescription", "npc_WingFear", "npc_WingDesire", "npc_WingMotivations", "npc_WingMentalState"]

        dominantDetail = npcDetail[22]
        wingDetail = npcDetail[25]
        LOD = npcDetail[27]

        self.npcVarDict.update(
            {promptVarNames[promptNamesCounter]: npcDetail[26]})
        promptNamesCounter += 1

        # Collect needed data from the generated NPC json file for the Dominant Type
        for keyword in keyWords:
            self.npcVarDict.update(
                {promptVarNames[promptNamesCounter]: dominantDetail.get(keyword)})
            promptNamesCounter += 1

        # Get Dominant Level of Development and remove the number at the start of the string to use for the Wing Level of Development
        dominantLOD = dominantDetail.get("levelOfDevelopment")
        self.npcVarDict.update(
            {promptVarNames[promptNamesCounter]: dominantLOD[LOD - 1]})
        promptNamesCounter += 1

        # Collect needed data from the generated NPC json file for the Wing Type
        for keyword in keyWords:
            self.npcVarDict.update(
                {promptVarNames[promptNamesCounter]: wingDetail.get(keyword)})
            promptNamesCounter += 1

        # Get Wing Level of Development
        wingLOD = wingDetail.get("levelOfDevelopment")
        self.npcVarDict.update(
            {promptVarNames[promptNamesCounter]: wingLOD[LOD - 1]})

        return

    def dataToPrompt(self):
        self.promptOutFileName = random.randint(10000, 19999)

        with open(f"prompts/{self.promptFile}", "r") as f:
            npcPrompt = f.read()

        self.npcPrompt = npcPrompt + str(self.npcVarDict)

        return

    def sendPrompt(self):
        # TODO: Figure out how to do this better
        openai.api_key = "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"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.npcPrompt,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )

        self.promptResponse = response

    def generatePrompt(self, npcDetail):
        self.detailToData(npcDetail)
        self.dataToPrompt()
        self.sendPrompt()
