import random
import json

from datetime import datetime

import LocationClass

from utility import utilities


def assignSN(NPC, mem_list):
    for member in mem_list:
        if NPC.NPC_UUID == member:
            NPC.NPC_Social_Network["data"] = mem_list
            break


def makeLocation():
    start = datetime.now()
    all_families = []

    test_town = LocationClass.Location()
    families = test_town.populate()

    for mem in families:
        s_network = LocationClass.SocialNetwork()
        s_network.populateAssociates(mem)
        all_families.append(s_network.families)

    # TODO: Help
    for NPC in reversed(test_town.citizens):
        for family in all_families:
            mem_list = family.get_dict()
            assignSN(NPC, mem_list)

    stop = datetime.now()
    time = stop - start

    r = random.randint(0, len(test_town.citizens))

    print(f"Location size: {test_town.size} \
          Time to create Location: {time} \
          Size of Location {utilities.getsize(test_town)} bytes")
    print(f"Randomly selected NPC: {test_town.citizens[r].NPC_UUID}")
    print(f"                       {test_town.citizens[r].NPC_Name}")

    citizens = test_town.citizens

    r = random.randint(0, len(citizens))
    person = citizens[r]
    person_out = {}
    graph = utilities.Graph()

# TODO: Figure out a way to build an serializable function within the graph
    for each in person.__dict__:
        current = person.__dict__[each]
        print(type(current))
        if type(current) is not type(graph):
            person_out.update({each: current})
        else:
            sn = {}
            for i in current:
                sn.update({i.id: i.get_connections()})
        person_out.update({each: person.__dict__[each]})

    return person_out


if __name__ == '__main__':
    makeLocation()
