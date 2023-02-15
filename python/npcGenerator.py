import logging

import npcInfoGenerator
import npcPromptGenerator
import npcGPTCall

# TODO: Add better logging everywhere


def npcGenerator():
    npcJSON = {}
    debug = False

    versionNum = "alpha-0.7.3"
    promptFile = "prompts/npcPrompt.txt"

    npcInfo = npcInfoGenerator.npcInfoGenerator()
    npcPrompt = npcPromptGenerator.npcDetailGenerator(promptFile)

    npcInfo.generateInfo()
    promptInfo = npcPrompt.generatePrompt(npcInfo.npcDetail)

    if debug:
        versionID = versionNum
        response = npcGPTCall.sendPrompt(promptInfo)
        responseText = response.choices[0].text
        responseList = responseText.splitlines()

        finalResponse = responseList[len(responseList) - 1]
        # print(finalResponse)

        npcJSON = npcInfo.npcPrintInfo()
        npcJSON.update({"Personality": finalResponse})
        npcJSON.update({"Version": versionID})
    else:
        versionID = f"{versionNum}-PROMPT_DEBUG"
        npcJSON = npcInfo.npcPrintInfo(debug)
        npcJSON.update({"Version": versionID})

    return npcJSON


if __name__ == "__main__":
    npcGenerator()
