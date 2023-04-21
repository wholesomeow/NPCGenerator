import math
import random

import NPCDetailData
import NPCDataCache
import NPCCommunicationClass

from utility import utilities


def defineOCEAN(CS_Coords, data):
    OCEAN = []
    OCEAN_Coords = data.OCEAN_Coords

    for i in OCEAN_Coords:
        OCEAN.append(
            int(math.dist(i, [-CS_Coords[0], -CS_Coords[1]]))
        )

    return OCEAN


def defineEnneagram(Enneagram_Data, data):
    # NOTE: Potentially update to use an Enum?
    Enneagram = {}
    r_Enneagram = random.randint(0, 8)
    r_Health = random.randint(0, 8)
    Centers = data.Enneagram_Centers
    keywords = data.Enneagram_Keywords

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


def defineMICE(data):
    MICE = {}
    MICE_Data = data.MICE_Data
    MICE_Tooltip = data.MICE_Tooltip

    r = random.randint(0, 3)
    MICE.update({
        "Data": MICE_Data[r],
        "Tooltip": MICE_Tooltip[r]
    })

    return MICE


def populateEM(data, main_data):
    EM = {}
    EM.update({
        "Enneagram": defineEnneagram(main_data, data),
        "MICE": defineMICE(data)
    })

    return EM


def defineCSData(data):
    CS_Data = {}
    CS_Coords = [0, 0]
    CS_Dimensions = data.CS_Dimensions
    CS_Tooltip = data.CS_Tooltip

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


def defineREIDimension(CS_Coords):
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


def populateCSREI(data):
    CS_Data = defineCSData(data)
    REI_Data = defineREIDimension(CS_Data["CSCoords"])
    CS_Data.update({"REIData": REI_Data})
    return CS_Data


class NPCBase:
    # Turns out you can set class level variables, who knew
    data_cache = NPCDataCache.CoreData
    main_data = data_cache().Enneagram_Main_Data
    sub_data = data_cache().Enneagram_Sub_Data
    data_detail = NPCDetailData

    def __init__(self, name, UUID, type=data_detail.NPCType.DEFAULT):
        self.NPC_Name = name
        self.NPC_UUID = UUID
        self.NPC_Social_Network = {
            "tooltip": "First iteration of elements is percieved relationship from source node to destination node. Second iteration of elements is percieved relationship from destination node to source node.",
            "data": None
        }
        self.NPC_CSREI = populateCSREI(self.data_cache)
        self.NPC_OCEAN = defineOCEAN(
            self.NPC_CSREI["CSCoords"], self.data_cache)
        self.NPC_EM = populateEM(self.data_cache, self.main_data)

        self.NPC_Communication = NPCCommunicationClass.NPCCommunicationBase()
        type_ID = self.NPC_EM["Enneagram"].get("typeID")
        self.NPC_Communication.loadInteractionMatrix(type_ID)

        self.NPC_Social_Role = None
        self.NPC_Detail_Information = self._createDetail()
        self.NPC_Communication = self.NPC_Communication.NPC_Interaction_Matrix
        self.NPC_Type = type.name

        self.NPC_Rumors = "None"
        self.NPC_Known_Jobs = "None"

    def _createDetail(self):
        NPC_Detail_Information = []
        # Creates generic details of NPC such as height, gender, and sexual ortientation
        num = [random.randint(1, 3), random.randint(1, 7)]

        self.NPC_Type = self.data_detail.NPCType.DEFAULT.name
        NPC_Sex = self.data_detail.SexType(num[0])
        NPC_Ori = self.data_detail.OrientationType(num[1])
        NPC_Ori_Tooltip = self.data_cache.Orientation_Tooltip[num[1] - 1]
        NPC_Gender = random.choice(list(self.data_detail.GenderType))

        Pronouns = self.data_cache.Pronouns
        r = random.randint(1, 2)

        match NPC_Gender.value:
            case 1:
                NPC_Pronoun = Pronouns["1"]
            case 2:
                NPC_Pronoun = Pronouns["2"]
            case 3:
                NPC_Pronoun = Pronouns[f"{r}"]
            case 4:
                NPC_Pronoun = Pronouns["4"]
            case 5:
                if r == 2:
                    r += 2
                NPC_Pronoun = Pronouns[f"{r}"]
            case 6:
                if r == 1:
                    r += 3
                NPC_Pronoun = Pronouns[f"{r}"]
            case 7:
                r = random.randint(1, 3)
                if r == 3:
                    NPC_Pronoun = Pronouns["4"]
                else:
                    NPC_Pronoun = Pronouns[f"{r}"]

        r_height = random.randint(0, 1)
        if r_height == 0:
            ft = random.randint(4, 7)
            inch = random.randint(0, 11)
            lbs = random.randint(110, 250)
        else:
            ft = random.randint(2, 3)
            inch = random.randint(0, 11)
            lbs = random.randint(75, 110)

        inches = (ft * 12) + inch

        # TODO: Combine the i2m function into a single return
        cm = utilities.imperialToMetric(inches, 0)
        kg = utilities.imperialToMetric(lbs, 1)
        Body_Type = self.data_detail.generateBodyType(cm, kg)
        NPC_Imperial_Data = [ft, inch, lbs]
        NPC_Metric_Data = [cm, kg]

        NPC_Detail_Information.append(NPC_Sex.name)
        NPC_Detail_Information.append(NPC_Ori.name)
        NPC_Detail_Information.append(NPC_Ori_Tooltip)
        NPC_Detail_Information.append(NPC_Gender.name)
        NPC_Detail_Information.append(NPC_Pronoun)
        NPC_Detail_Information.append(Body_Type)
        NPC_Detail_Information.append(NPC_Imperial_Data)
        NPC_Detail_Information.append(NPC_Metric_Data)

        return NPC_Detail_Information

    def createRumorsKnown(self):
        # Needs Encounter-style State Machine functionality
        #  aka Quest Generator
        pass

    def createJobsKnown(self):
        # Needs Encounter-style State Machine functionality
        #  aka Quest Generator
        pass

    # TODO: Create getters and setters for editing parts of the NPC
