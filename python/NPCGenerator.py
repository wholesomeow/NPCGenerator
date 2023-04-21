import random

from datetime import datetime

import NPCClass
import LocationClass

from utility import utilities
from nameGen import markovChain


def assignSN(NPC, mem_list):
    for member in mem_list:
        if NPC.NPC_UUID == member:
            NPC.NPC_Social_Network["data"] = mem_list
            break


def makeLocation(size=8):
    """Use to build a new collection of NPCs in a location.

    Arguments:
    Size(int) dictates the amount of people to be created in the location.
    Standard sizes are 100, 1000, 6000, 20000. Size will default
    to 8 - for testing purposes - if no other value is specified."""

    start = datetime.now()
    all_networks = []
    citizens = []

    test_town = LocationClass.Location(size)
    counter = start.year * 10000000000 + start.month * 100000000 + \
        start.day * 1000000 + start.hour * 10000 + start.minute * 100 + start.second
    IDS = [utilities.encode(counter + 1) for i in range(size)]
    names = [markovChain.MarkovChain().getName() for i in range(size)]

    for i in range(size):
        NPC = NPCClass.NPCBase(names[i], IDS[i])
        citizens.append(NPC)
        test_town.citizens.append(NPC)

    families = test_town.buildFamilies(citizens)

    for mem in families:
        s_network = LocationClass.SocialNetwork(test_town)
        s_network.populateAssociates(mem)
        all_networks.append(s_network.networks)

    for NPC in reversed(test_town.citizens):
        for network in all_networks:
            mem_list = network.get_dict()
            assignSN(NPC, mem_list)

    stop = datetime.now()
    time = stop - start

    r = random.choice(test_town.citizens)

    print(f"Location size: {size} \
          Time to create Location: {time} \
          Size of Location ~{round(utilities.getObjSize(test_town) / 1000000)} MB")
    print(f"Random NPC UUID: {r.NPC_UUID}")
    print(f"Random NPC Name: {r.NPC_Name}")

    person = random.choice(test_town.citizens)

    # for each in person.__dict__:
    #     person_out.update({each: person.__dict__[each]})

    return person.__dict__


if __name__ == '__main__':
    makeLocation(250)  # 1500 is around the population size of Skyrim
