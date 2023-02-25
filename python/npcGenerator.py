import logging
from datetime import datetime

import npcInfoGenerator
import npcPromptGenerator
import npcGPTCall

# TODO: Add better logging everywhere


def sendPromptCompile(promptCompileInfo, engine):
    responseDict = npcGPTCall.sendPrompt(promptCompileInfo, engine)

    usageCompile = responseDict.get("Usage")
    responseCompile = responseDict.get("Response")

    return usageCompile, responseCompile


def sendPromptCreate(promptCreateInfo, engine):
    responseDict = npcGPTCall.sendPrompt(promptCreateInfo, engine)

    usageCreate = responseDict.get("Usage")
    responseCreate = responseDict.get("Response")

    return usageCreate, responseCreate


def npcGenerator():
    npcJSON, stats = {}, {}
    firstPrompt, secondPrompt = [], []
    debug = False

    versionNum = "alpha-0.8.0"
    promptFileCompile = "prompts/npcPromptCompile.txt"
    promptFileCreate_1 = "prompts/npcPromptCreate_1.txt"
    promptFileCreate_2 = "prompts/npcPromptCreate_2.txt"

    tstart = datetime.now()

    npcInfo = npcInfoGenerator.npcInfoGenerator()
    npcPrompt = npcPromptGenerator.npcDetailGenerator(
        promptFileCompile, promptFileCreate_1, promptFileCreate_2)

    npcInfo.generateInfo()

    if not debug:
        versionID = versionNum

        # Generate and send Prompt for initial data compiliation
        # Set GPT-3 Engine to Davinci
        engine = 0
        npcPrompt.generatePromptCompile(npcInfo.npcDetail)
        usageCompile, responseCompile = sendPromptCompile(
            npcPrompt.npcPromptOut, engine)
        npcPrompt.storeData(responseCompile)
        firstPrompt.extend((npcPrompt.npcStoredData[0],
                            npcPrompt.npcStoredData[1],
                            npcPrompt.npcStoredData[2],
                            npcInfo.npcDetail[27],
                            npcPrompt.npcStoredData[5]))

        # Generate and send Prompt for part one of novel data creation
        # Set GPT-3 Engine to Curie
        # engine = 1
        npcPrompt.generatePromptCreate_1(firstPrompt)
        usageCreate_1, responseCreate_1 = sendPromptCreate(
            npcPrompt.npcPromptOut_1, engine)
        npcPrompt.storeData(responseCreate_1)
        secondPrompt.extend(
            (npcPrompt.npcStoredData[8], npcPrompt.npcStoredData[5]))

        # Generate and send Prompt for part two of novel data creation
        npcPrompt.generatePromptCreate_2(secondPrompt)
        usageCreate_2, responseCreate_2 = sendPromptCreate(
            npcPrompt.npcPromptOut_2, engine)
        npcPrompt.storeData(responseCreate_2)

        tend = datetime.now()

        tTotal = tend - tstart

        stats.update({"TotalTime": tTotal.seconds})
        stats.update({"UsageCompile": usageCompile})
        stats.update({"UsageCreate_1": usageCreate_1})
        stats.update({"UsageCreate_2": usageCreate_2})

        npcJSON = npcInfo.npcPrintInfo()
        npcJSON.update({"Response_Total": npcPrompt.npcStoredData})
        npcJSON.update({"Stats": stats})
        npcJSON.update({"Version": versionID})
    else:

        tend = datetime.now()

        versionID = f"{versionNum}-PROMPT_DEBUG"
        npcJSON = npcInfo.npcPrintInfo(debug)
        npcJSON.update({"PromptInfo": npcPrompt.npcPromptData})
        npcJSON.update({"TotalTime": tTotal.seconds})
        npcJSON.update({"Version": versionID})

    return npcJSON


if __name__ == "__main__":
    npcGenerator()
