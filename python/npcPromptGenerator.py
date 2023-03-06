import logging


class npcPromptGenerator:
    def __init__(self):
        self.npcPromptData = []
        self.promptResponse = {}

    def generatePrompt(promptFile, promptData):
        with open(f"{promptFile}", "r") as f:
            npcPrompt = f.read()

        npcPromptOut = npcPrompt + str(promptData)

        return npcPromptOut
