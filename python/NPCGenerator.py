import random
import json

from datetime import datetime
from multiprocessing import Pool

import LocationClass

from utility import utilities


def assignSN(NPC, mem_list):
    for member in mem_list:
        if NPC.NPC_UUID == member:
            NPC.NPC_Social_Network["data"] = mem_list
            break


def makeLocation():
    start = datetime.now()
    all_networks = []
    citizens = []
    items = []
    counter = start.year * 10000000000 + start.month * 100000000 + \
        start.day * 1000000 + start.hour * 10000 + start.minute * 100 + start.second

    test_town = LocationClass.Location()
    with Pool() as pool:
        items = [counter + i for i in range(test_town.size)]
        NPC_List = [pool.map(test_town.populate, items)
                    for i in range(test_town.size)]
        for NPC in NPC_List[0]:
            citizens.append(NPC)
            test_town.citizens.append(NPC)

        families = test_town.buildFamilies(citizens)

    for mem in families:
        s_network = LocationClass.SocialNetwork(test_town)
        s_network.populateAssociates(mem)
        all_networks.append(s_network.networks)

    # TODO: Help
    for NPC in reversed(test_town.citizens):
        for network in all_networks:
            mem_list = network.get_dict()
            assignSN(NPC, mem_list)

    stop = datetime.now()
    time = stop - start

    r = random.randint(0, len(test_town.citizens) - 1)

    print(f"Location size: {test_town.size} \
          Time to create Location: {time} \
          Size of Location {utilities.getsize(test_town) / int(1024^2)} MB")
    print(f"Randomly selected NPC: {test_town.citizens[r].NPC_UUID}")
    print(f"                       {test_town.citizens[r].NPC_Name}")

    r = random.randint(0, len(test_town.citizens))
    person = test_town.citizens[r]

    # for each in person.__dict__:
    #     person_out.update({each: person.__dict__[each]})

    return person.__dict__


if __name__ == '__main__':
    makeLocation()
