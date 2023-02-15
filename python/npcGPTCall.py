import openai
import logging


def sendPrompt(npcPrompt):
    # TODO: Replace env variable key with key from secrets managament
    with open("secrets", "r") as file:
        keyString = file.read()

    openai.api_key = keyString

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=npcPrompt,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    return response


if __name__ == '__main__':
    sendPrompt()
