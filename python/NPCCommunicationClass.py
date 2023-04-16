import json

import NPCDataCache
from utility import utilities


class NPCCommunicationBase:
    def __init__(self):
        self.NPC_Interaction_Matrix = []

    def loadInteractionMatrix(self, type_ID):
        """Loads an interaction matrix specific to the NPC Enneagram type
           and how they form relationships with other Enneagram types."""
        subData = NPCDataCache.CoreData().Enneagram_Sub_Data
        for i in subData:
            compat = i.get("compatibilityMatrix")
            if type_ID in compat:
                self.NPC_Interaction_Matrix.append(i)
            if len(self.NPC_Interaction_Matrix) == 9:
                break


class NPCInteractions():
    def __init__(self):
        self.NPC_Emotions_Tree = None

    def createEmotionsTree(self):
        """Creates a tree consisting of main emotions, subtypes, and sub-subtypes"""
        Root_Emotions = NPCDataCache.CoreData().Root_Emotions
        Child_Emotions = NPCDataCache.CoreData().Child_Emotions
        G_Child_Emotions = NPCDataCache.CoreData().G_Child_Emotions

        self.NPC_Emotions_Tree = utilities.Tree(Root_Emotions, Child_Emotions)
        for i, v in enumerate(self.NPC_Emotions_Tree):
            for j, w in enumerate(v):
                self.NPC_Emotions_Tree[i][j].attach(G_Child_Emotions[0])
                del G_Child_Emotions[0]

        return

    def interactionResponse(self):
        pass
