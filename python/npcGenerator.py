import logging

import npcInfoGenerator
import npcPromptGenerator

# TODO: Add better logging everywhere


def npcGenerator():
    npcJSON = {}

    versionID = "alpha-0.6.1"
    promptFile = "prompts/npcPrompt.txt"

    npcInfo = npcInfoGenerator.npcInfoGenerator()
    npcPrompt = npcPromptGenerator.npcDetailGenerator(promptFile)

    npcInfo.generateInfo()
    npcPrompt.generatePrompt(npcInfo.npcDetail)

    response = npcPrompt.promptResponse
    responseText = response.choices[0].text
    responseList = responseText.splitlines()

    finalResponse = responseList[len(responseList) - 1]
    # print(finalResponse)

    npcJSON = npcInfo.npcPrintInfo()
    npcJSON.update({"Personality": finalResponse})

    return npcJSON


if __name__ == "__main__":
    npcGenerator()
