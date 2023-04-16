import random

import NPCClass

from utility import utilities
from nameGen import markovChain

from datetime import datetime
from enum import Flag, Enum
from collections import deque, defaultdict
from itertools import combinations


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
    def __init__(self, size=Size.HAMLET):
        self.size = size.value
        self.type = size.name
        self.families = deque()
        self.citizens = deque()
        self.family_size = {
            "Parents": 2,
            "Kids": 2
        }

    def buildFamilies(self, people):
        members = {}
        for i in self.family_size:
            collection = []
            current_size = self.family_size[i]
            for j in range(current_size):
                collection.append(people.popleft())
            members.update({i: collection})
        return members

    def populate(self):
        families, citizens = deque(), deque()
        now = datetime.now()
        counter = now.year * 10000000000 + now.month * 100000000 + \
            now.day * 1000000 + now.hour * 10000 + now.minute * 100 + now.second

        MC = markovChain.MarkovChain()

        for i in range(self.size):
            counter += i
            UUID = utilities.encode(counter)
            Name = MC.getName()
            NPC = NPCClass.NPCBase(UUID, Name)
            NPC.assignCoreData()
            NPC.assignCommunication()
            NPC.createDetail()

            self.citizens.append(NPC)
            citizens.append(NPC)

        total_size = 0
        for i in self.family_size:
            total_size += self.family_size[i]
        family_amount = int(self.size / total_size)

        for i in range(family_amount):
            members = self.buildFamilies(citizens)
            families.append(members)

        return families

    def getCitizen(self, id):
        for person in self.citizens:
            if person.UUID is id:
                return person


class SocialNetwork:
    def __init__(self):
        self.families = deque()

    def populateAssociates(self, members):
        # First, create graph of family members
        arr = []
        family = utilities.Graph()

        for current_role in members:
            for person in members[current_role]:
                match current_role:
                    case "Parents":
                        person.NPC_Social_Role = Genogram.PARENT | Genogram.SPOUSE
                    case "Kids":
                        person.NPC_Social_Role = Genogram.CHILD | Genogram.SIBLING
                family.add_vertex(person.NPC_UUID)
                arr.append(person.NPC_UUID)

        # Built a list of all posible direct connections within the family
        combs = list(combinations(arr, 2))

        for combo in combs:
            r = random.randint(0, 5)
            family.add_edge(combo[0], combo[1],
                            [Closeness.FAMILY, Relationship(r)])

        self.families.append(family)
