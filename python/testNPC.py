import npcInfoGenerator
import npcPromptGenerator


def main():
    # Write code for testing either the Information Generator or the Prompt Generator here
    promptFile = "prompts/npcPrompt.txt"

    npcInfo = npcInfoGenerator.npcInfoGenerator()
    npcPrompt = npcPromptGenerator.npcDetailGenerator(promptFile)

    npcInfo.generateInfo()
    npcPrompt.testFile(npcInfo.npcDetail)

    print("Done")


if __name__ == "__main__":
    main()
