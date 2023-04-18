import random
import itertools

import NPCClass

from utility import utilities
from nameGen import markovChain

from datetime import datetime
from enum import Flag, Enum


class Genogram(Flag):
    DEFAULT = 0
    PARENT = 1
    SIBLING = 2
    SPOUSE = 4
    GRAND = 8
    STEP = 16
    OLDER = 32
    OLDEST = 64
    YOUNGER = 128
    YOUNGEST = 256
    CHILD = 512
    INLAW = 1024
    NIBLING = 2048
    MATERNAL = 4096
    PATERNAL = 8192


class Relationship(Enum):
    NONE = 0
    TERRIBLE = 1
    BAD = 2
    OKAY = 3
    GOOD = 4
    GREAT = 5


class Closeness(Enum):
    AQUAINTANCE = 1     # Someone you know of
    ASSOCIATE = 2       # An aquaintance you are more familiar with
    FRIEND = 3          # A Friend
    CLOSEFRIEND = 4     # The majority of someones friend group
    GOODFRIEND = 5      # The closest circle of friends
    FAMILY = 6          # Family members, but Relationship is not const


class Size(Enum):
    TEST = 8
    HAMLET = 100
    VILLAGE = 1000
    TOWN = 6000
    CITY = 20000


class Location:
    def __init__(self, size=Size.TEST):
        self.size = size.value
        self.type = size.name
        self.families = []
        self.citizens = []
        self.family_size = {
            "Parents": 2,
            "Kids": 2
        }
        total = [self.family_size[i] for i in self.family_size]
        self.family_total = sum(total)
        self.family_amount = int(self.size / self.family_total)
        self.MC = markovChain.MarkovChain()

    def _buildFamilies(self, citizens):
        members = {}
        for i in self.family_size:
            collection = []
            if self.family_size[i] == "Total":
                break
            current_size = self.family_size[i]
            for j in range(current_size):
                if len(citizens) > 0:
                    collection.append(citizens.pop())
            members.update({i: collection})
        return members

    def buildFamilies(self, citizens):
        families = []
        for i in range(self.family_amount):
            members = self._buildFamilies(citizens)
            families.append(members)

        return families

    def populate(self, counter):
        name = self.MC.getName()
        UUID = utilities.encode(counter)
        NPC = NPCClass.NPCBase(UUID, name)
        NPC.assignCoreData()
        NPC.assignCommunication()
        NPC.createDetail()

        return NPC

    def getCitizen(self, id):
        for person in self.citizens:
            if person.NPC_UUID is id:
                return person


class SocialNetwork:
    def __init__(self, test_town):
        self.networks = []
        self.location = test_town

    def getRole(self, person, num):
        role = f"Role_{num}"
        return person.NPC_Social_Role[role]

    def populateAssociates(self, members):
        # First, create graph of family members
        arr = []
        network = utilities.Network()

        for current_role in members:
            for person in members[current_role]:
                match current_role:
                    case "Parents":
                        person.NPC_Social_Role = {
                            "Role_1": Genogram.PARENT.name,
                            "Role_2": Genogram.SPOUSE.name
                        }
                    case "Kids":
                        person.NPC_Social_Role = {
                            "Role_1": Genogram.CHILD.name,
                            "Role_2": Genogram.SIBLING.name
                        }
                network.add_vertex(person.NPC_UUID)
                arr.append(person.NPC_UUID)

        # Built a list of all posible direct connections within the family
        # ---
        # itertools and list comprehension is shockingly faster than for loops
        # TODO: Replace for loops with iter/comprehension where possible/able
        combs = [c for c in itertools.product(
            arr, arr) if len(set(c)) == len(c)]

        # TODO: Add in Relationship_To value in the weight to indicate what the relationship to the src node is
        for combo in combs:
            r = random.randint(0, 5)
            c_1 = self.location.getCitizen(combo[0])
            c_2 = self.location.getCitizen(combo[1])

            # Check the relationship status between nodes to get relationship type
            if self.getRole(c_1, 1) == self.getRole(c_2, 1):
                Relationship_Type = f"{self.getRole(c_1, 2)} to {self.getRole(c_2, 2)}"
            else:
                Relationship_Type = f"{self.getRole(c_1, 1)} to {self.getRole(c_2, 1)}"

            network.add_edge(combo[0], combo[1],
                             [Closeness.FAMILY.name,
                              Relationship_Type,
                              Relationship(r).name]
                             )

        # Second, add random friend connections to each network

        # Last, search one layer deep in friend network and add to player network
        self.networks = network
