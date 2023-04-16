import logging
from datetime import datetime

import npcClass


def npcGenerator():
    npcJSON, response = {}, {}

    versionID = "alpha-0.9.4"
    promptFile1 = "prompts/npcPromptCompile.txt"
    promptFile2 = "prompts/npcPromptCreate_1.txt"
    promptFile3 = "prompts/npcPromptCreate_2.txt"

    tstart = datetime.now()

    NPC = npcClass.NPC()
    NPC.createNPC()

    # Generate and send Prompt for initial data compiliation
    # 0 = GPT-3, 1 = Curie, 2 = ChatGPT
    response1, usage1 = NPC.getPromptResponse(
        promptFile1,
        NPC.Enneagram, 0
    )

    NPC.updateNPCResponse(response1, 0)

    # Generate and send Prompt for part one of novel data creation
    promptData = NPC.buildPromptData(1)

    response2, usage2 = NPC.getPromptResponse(
        promptFile2,
        promptData, 0
    )

    NPC.updateNPCResponse(response2, 1)

    # Generate and send Prompt for part two of novel data creation
    promptData = NPC.buildPromptData(2)

    response3, usage3 = NPC.getPromptResponse(
        promptFile3,
        promptData, 0
    )

    NPC.updateNPCResponse(response3, 2)

    tend = datetime.now()

    tTotal = tend - tstart

    npcJSON.update({"NPCData": NPC.NPCData})
    npcJSON.update({"Prompt1Usage": usage1})
    npcJSON.update({"Prompt2Usage": usage2})
    npcJSON.update({"Prompt3Usage": usage3})
    npcJSON.update({"TotalTime": tTotal.seconds})

    return npcJSON


if __name__ == "__main__":
    npcGenerator()
