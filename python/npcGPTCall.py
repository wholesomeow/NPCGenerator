import openai
import logging


def remove_empty_strings(responseList):
    return list(filter(lambda x: x != "", responseList))


def remove_blank_strings(responseList):
    return list(filter(lambda x: x != " ", responseList))


def sendPrompt(npcPrompt, engine=1):
    responseDict = {}
    # TODO: Replace env variable key with key from secrets managament
    with open("secrets", "r") as file:
        keyString = file.read()

    openai.api_key = keyString

    if engine == 0:
        # Use DaVinci for longer prompts
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=npcPrompt,
            max_tokens=1700,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )
    elif engine == 1:
        # Use Curie for shorter prompts
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=npcPrompt,
            max_tokens=1300,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )

    responseText = response.choices[0].text
    usage = response.usage
    responseList = responseText.splitlines()

    responseListClean = remove_empty_strings(responseList)
    responseClean = remove_blank_strings(responseListClean)

    responseDict.update({"Usage": usage})
    responseDict.update({"Response": responseClean})

    return responseDict


if __name__ == '__main__':
    sendPrompt()
