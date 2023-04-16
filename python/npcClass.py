import random

import NPCCoreData
import NPCDetailData
import NPCDataCache
import NPCCommunicationClass

from utility import utilities

from collections import deque


class NPCBase:
    def __init__(self, UUID, Name) -> None:
        self.NPC_UUID = UUID
        self.NPC_Name = Name
        self.NPC_Detail_Information = deque()
        self.NPC_Social_Network = None

        self.NPC_Social_Role = None

        self.NPC_Type = None
        self.NPC_OCEAN = None
        self.NPC_CSREI = None
        self.NPC_EM = None

        self.NPC_Communication = None

        self.NPC_Rumors = None
        self.NPC_Known_Jobs = None

    def assignCoreData(self):
        NPC_CSREI = NPCCoreData.CSREI()
        NPC_OCEAN = NPCCoreData.OCEAN()
        NPC_EM = NPCCoreData.EM()

        NPC_CSREI.populateCSREI()
        NPC_OCEAN.defineOCEAN(NPC_CSREI.CSREI[0])
        NPC_EM.populateEM()

        self.NPC_CSREI = NPC_CSREI.__dict__
        self.NPC_OCEAN = NPC_OCEAN.__dict__
        self.NPC_EM = NPC_EM.__dict__

    def assignCommunication(self):
        # Composes the Communication Class to the NPC Class
        NPC_Communication = NPCCommunicationClass.NPCCommunicationBase()
        EM_Data = self.NPC_EM.get("EM")
        type_ID = EM_Data[0].get("typeID")
        NPC_Communication.loadInteractionMatrix(type_ID)

        self.NPC_Communication = NPC_Communication.__dict__

    def createDetail(self):
        # Creates generic details of NPC such as height, gender, and sexual ortientation
        num = deque([3, 7])
        for index, each in enumerate(num):
            num[index] = random.randint(1, each)

        self.NPC_Type = NPCDetailData.NPCType.DEFAULT
        NPC_Sex = NPCDetailData.SexType(num[0])
        NPC_Ori = NPCDetailData.OrientationType(num[1])
        NPC_Ori_Tooltip = NPCDataCache.CoreData(
        ).Orientation_Tooltip[num[1] - 1]
        NPC_Gender = random.choice(list(NPCDetailData.GenderType))

        Pronouns = NPCDataCache.CoreData().Pronouns
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

        cm = utilities.imperialToMetric(inches, 0)
        kg = utilities.imperialToMetric(lbs, 1)
        Body_Type = NPCDetailData.generateBodyType(cm, kg)
        NPC_Imperial_Data = deque([ft, inch, lbs])
        NPC_Metric_Data = deque([cm, kg])

        self.NPC_Detail_Information.append(NPC_Sex.name)
        self.NPC_Detail_Information.append(NPC_Ori.name)
        self.NPC_Detail_Information.append(NPC_Ori_Tooltip)
        self.NPC_Detail_Information.append(NPC_Gender.name)
        self.NPC_Detail_Information.append(NPC_Pronoun)
        self.NPC_Detail_Information.append(Body_Type)
        self.NPC_Detail_Information.append(NPC_Imperial_Data)
        self.NPC_Detail_Information.append(NPC_Metric_Data)

    def createRumorsKnown(self):
        # Needs Encounter-style State Machine functionality
        #  aka Quest Generator
        pass

    def createJobsKnown(self):
        # Needs Encounter-style State Machine functionality
        #  aka Quest Generator
        pass

    # TODO: Create getters and setters for editing parts of the NPC
