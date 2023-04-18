import json

from dataclasses import dataclass


@dataclass
class CoreData:
    def __init__(self):
        try:
            with open("json/keywordEnneagramData.json", "r") as e:
                data = json.load(e)
                self.Enneagram_Main_Data = data.get("mainData")
                self.Enneagram_Sub_Data = data.get("subData")
        except IOError:
            print("Could not load file")

    OCEAN_Coords = [[-100, -0],
                    [100, 100],
                    [-100, 100],
                    [100, 0],
                    [-0, -100]]

    # Centers are        Thinking,   Feeling,  Instinctive
    Enneagram_Centers = [[5, 6, 7], [2, 3, 4], [1, 8, 9]]
    Enneagram_Keywords = ["typeID", "briefDesc", "basicFear",
                          "basicDesire", "keyMotivations", "addictions"]

    MICE_Data = [
        "Money",
        "Ideology",
        "Coercion",
        "Ego"
    ]

    MICE_Tooltip = [
        "for financial compensation, with the amount depending on risk and desperation.",
        "for advancement with a cause they believe in, or against a cause they despise.",
        "by aggressive or violent means - typically physical/emotional bullying or blackmail.",
        "to inflate or validate their ego - either by undermining opponents or by highlighting their success."
    ]

    CS_Dimensions = [
        "Versatile",
        "Analytical",
        "Indifferent",
        "Intuitive"
    ]

    CS_Tooltip = [
        "is both a rational and intuitive person.",
        "is a rational person, but not very intuitive.",
        "is neither a very rational person, nor very intuitive.",
        "is a intuitive person, but not very rational."
    ]

    Root_Emotions = [
        ["Anger"], ["Disgust"], ["Sad"],
        ["Happy"], ["Surprise"], ["Fear"]
    ]

    Child_Emotions = [
        [["Hurt"], ["Threatened"], ["Hateful"], ["Mad"],
            ["Aggressive"], ["Frustrated"], ["Distant"], ["Critical"]],
        [["Disaproval"], ["Disapointed"], ["Awful"], ["Avoidance"]],
        [["Guilty"], ["Abandoned"], ["Despair"],
            ["Depressed"], ["Lonely"], ["Bored"]],
        [["Optimistic"], ["Intimate"], ["Peaceful"], ["Powerful"],
            ["Accepted"], ["Proud"], ["Interested"], ["Joyful"]],
        [["Excited"], ["Amazed"], ["Confused"], ["Startled"]],
        [["Scared"], ["Anxious"], ["Insecure"],
            ["Submissive"], ["Rejected"], ["Humiliated"]],
    ]

    G_Child_Emotions = [
        [["Embarrassed"], ["Devistated"]],
        [["Insecure"], ["Jealous"]],
        [["Resentful"], ["Violated"]],
        [["Furious"], ["Enraged"]],
        [["Provoked"], ["Hostile"]],
        [["Infuriated"], ["Irritated"]],
        [["Withdrawn"], ["Suspicious"]],
        [["Skeptical"], ["Sarcastic"]],
        [["Judgemental"], ["Loathing"]],
        [["Repugnant"], ["Revolted"]],
        [["Revulsion"], ["Detestable"]],
        [["Aversion"], ["Hesitant"]],
        [["Remoresful"], ["Ashamed"]],
        [["Ignored"], ["Victimized"]],
        [["Powerless"], ["Vulnerable"]],
        [["Inferior"], ["Empty"]],
        [["Abandoned"], ["Isolated"]],
        [["Apathetic"], ["Indifferent"]],
        [["Inspired"], ["Open"]],
        [["Playful"], ["Sensitive"]],
        [["Hopeful"], ["Loving"]],
        [["Provocative"], ["Courageous"]],
        [["Fulfilled"], ["Respected"]],
        [["Confident"], ["Important"]],
        [["Inquisitive"], ["Amused"]],
        [["Estatic"], ["Liberated"]],
        [["Energetic"], ["Eager"]],
        [["Awe"], ["Astonished"]],
        [["Perplexed"], ["Disillusoned"]],
        [["Dismayed"], ["Shocked"]],
        [["Terrified"], ["Frightened"]],
        [["Overwhelmed"], ["Worried"]],
        [["Inadequate"], ["Inferior"]],
        [["Worthless"], ["Insignificant"]],
        [["Inadequate"], ["Alientated"]],
        [["Disrespected"], ["Ridiculed"]]
    ]

    Orientation_Tooltip = [
        "Not sexually attracted to anyone.",
        "Not romantically attracted to anyone.",
        "Attracted to the sex/gender opposite their own on the spectrum.",
        "Doesn't experience sexual attraction to someone unless they have a deep, emotional connection with them.",
        "Attracted to the sex/gender on the same side of the spectrum.",
        "Attracted to more than one gender or gender identity.",
        "Attracted to the person rather than their sex, gender, or gender identity."
    ]

    Pronouns = {
        "1": "He Him",
        "2": "She Her",
        "4": "They Them"}
