import math
import json
import random

import NPCDataCache


class OCEAN:
    def __init__(self):
        self.OCEAN = []

    def defineOCEAN(self, CS_Coords):
        OCEAN_Coords = NPCDataCache.CoreData().OCEAN_Coords

        for i in OCEAN_Coords:
            self.OCEAN.append(
                int(math.dist(i, [-CS_Coords[0], -CS_Coords[1]]))
            )

        return self.OCEAN


class EM:
    def __init__(self):
        self.EM = {}

    def defineEnneagram(self, Enneagram_Data):
        # NOTE: Potentially update to use an Enum?
        Enneagram = {}
        dominantEmotion = ""
        r_Enneagram = random.randint(0, 8)
        r_Health = random.randint(0, 8)
        Centers = NPCDataCache.CoreData().Enneagram_Centers
        keywords = NPCDataCache.CoreData().Enneagram_Keywords

        if r_Enneagram + 1 in Centers[0]:
            dominantEmotion = "Fear"
        elif r_Enneagram + 1 in Centers[1]:
            dominantEmotion = "Shame"
        elif r_Enneagram + 1 in Centers[2]:
            dominantEmotion = "Anger"

        levels = Enneagram_Data[r_Enneagram].get("levelOfDevelopment")
        LOD = levels[r_Health]

        for word in keywords:
            Enneagram.update({word: Enneagram_Data[r_Enneagram].get(word)})
        Enneagram.update({"dominantEmotion": dominantEmotion})
        Enneagram.update({"levelOfDevelopment": {"levelValue": r_Health,
                                                 "LOD": LOD}})

        return Enneagram

    def defineMICE(self):
        MICE = {}
        MICE_Data = NPCDataCache.CoreData().MICE_Data
        MICE_Tooltip = NPCDataCache.CoreData().MICE_Tooltip

        r = random.randint(0, 3)
        MICE.update({
            "Data": MICE_Data[r],
            "Tooltip": MICE_Tooltip[r]
        })

        return MICE

    def populateEM(self):
        Enneagram = {}
        MICE = {}

        Enneagram_Data = NPCDataCache.CoreData().Enneagram_Main_Data
        Enneagram = self.defineEnneagram(Enneagram_Data)
        MICE = self.defineMICE()
        self.EM.update({
            "Enneagram": Enneagram,
            "MICE": MICE
        })

        return self.EM


class CSREI:
    def __init__(self):
        self.CSREI = {}

    def defineCSData(self):
        CS_Data = {}
        CS_Coords = [0, 0]
        CS_Dimensions = NPCDataCache.CoreData().CS_Dimensions
        CS_Tooltip = NPCDataCache.CoreData().CS_Tooltip

        CS_Coords[0] = random.randint(-100, 100)
        CS_Coords[1] = random.randint(-100, 100)
        CS_Data.update({"CSCoords": CS_Coords})

        if CS_Coords[0] <= 0 and CS_Coords[1] <= 0:
            CS_Data.update({"Dimension": CS_Dimensions[0]})
            CS_Data.update({"Tooltip": CS_Tooltip[0]})
        elif CS_Coords[0] <= 0 and CS_Coords[1] >= 0:
            CS_Data.update({"Dimension": CS_Dimensions[1]})
            CS_Data.update({"Tooltip": CS_Tooltip[1]})
        elif CS_Coords[0] >= 0 and CS_Coords[1] >= 0:
            CS_Data.update({"Dimension": CS_Dimensions[2]})
            CS_Data.update({"Tooltip": CS_Tooltip[2]})
        elif CS_Coords[0] >= 0 and CS_Coords[1] <= 0:
            CS_Data.update({"Dimension": CS_Dimensions[3]})
            CS_Data.update({"Tooltip": CS_Tooltip[3]})

        return CS_Data

    def defineREIDimension(self, CS_Coords):
        REI_Data = ""

        if CS_Coords[0] >= 0 and abs(CS_Coords[0]) > abs(CS_Coords[1]):
            REI_Data = "information collecting skills"
        if CS_Coords[0] <= 0 and abs(CS_Coords[0]) > abs(CS_Coords[1]):
            REI_Data = "action taking skills"
        if CS_Coords[1] >= 0 and abs(CS_Coords[0]) < abs(CS_Coords[1]):
            REI_Data = "interpersonal communication skills"
        if CS_Coords[1] <= 0 and abs(CS_Coords[0]) < abs(CS_Coords[1]):
            REI_Data = "information analysis skills"

        return REI_Data

    def populateCSREI(self):
        CS_Data = self.defineCSData()
        REI_Data = self.defineREIDimension(CS_Data["CSCoords"])
        CS_Data.update({"REIData": REI_Data})
        self.CSREI = CS_Data
