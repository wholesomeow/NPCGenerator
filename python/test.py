import random
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
from collections import deque

import NPCClass
import NPCCoreData
import LocationClass
from utility import utilities


def testCSREI():
    # TEST SUCCESS
    # Generate Coordinates
    CSREI = NPCCoreData.CSREI().defineCSData()
    x = CSREI[0][0]
    y = CSREI[0][1]

    if x >= 0 and abs(x) > abs(y):
        REI_Dimension = "Information Skills"
    if x <= 0 and abs(x) > abs(y):
        REI_Dimension = "Action Skills"
    if y >= 0 and abs(x) < abs(y):
        REI_Dimension = "Interpersonal Skills"
    if y <= 0 and abs(x) < abs(y):
        REI_Dimension = "Analytical Skills"

    print(f"X: {x} Y: {y} | {REI_Dimension}")

    return CSREI


def testOCEAN(CSREI):
    # TEST SUCCESSFULL
    OCEAN = NPCCoreData.OCEAN().defineOCEAN(CSREI[0])

    print(CSREI)
    print(OCEAN)

    for i in OCEAN:
        j = i / 10
        s = "X" * int(j)
        print(s)

    OCEAN_Coords = [
        [-100, -0],
        [100, 100],
        [-100, 100],
        [100, 0],
        [-0, -100]
    ]

    # Plot Code
    x = CSREI[0][0]
    y = CSREI[0][1]

    x1 = np.linspace(-100, 100, 100)
    y1 = x1

    #  OCEAN Lines
    x2 = np.linspace(-100, 100, 100)
    y2 = np.linspace(-0, 0, 100)

    plt.title("REI Dimensions from CS Coordinates")
    plt.xlabel("Rationality")
    plt.ylabel("Intuition")

    # True CS_Coords
    plt.plot(x1, y1, 'Blue')
    plt.plot(y1, -x1, 'Blue')
    plt.plot(x, y,
             marker="o",
             markersize=5,
             markeredgecolor="black",
             markerfacecolor="red")

    # Inverse CS_Coords
    plt.plot(-x, -y,
             marker="o",
             markersize=5,
             markeredgecolor="red",
             markerfacecolor="black")

    plt.plot(x2, y2, 'Red')
    plt.plot(y2, x2, 'Red')

    # Plot OCEAN Lines
    for i in OCEAN_Coords:
        plt.plot(
            np.linspace(x, i[0]),
            np.linspace(y, i[1]),
            "black"
        )

    plt.grid()
    plt.show()


def testMakeNPC():
    # TEST SUCCESSFULL
    location = []
    target = 100
    counter = 100000000000

    start = datetime.now()

    for i in range(target):
        counter += i
        UUID = utilities.encode(counter)
        NPC = NPCClass.NPCBase(UUID)
        NPC.assignCoreData()
        NPC.assignCommunication()
        NPC.createDetail()
        location.append(NPC)

    stop = datetime.now()
    time = stop - start

    # for i in NPC.__dict__:
    #     print(NPC.__dict__[i])

    print(f"Target size: {target} \
          Time to create NPCs: {time} \
          Size of Location {utilities.getsize(location)} bytes")


def makeLocation():
    start = datetime.now()
    all_families = deque()

    test_town = LocationClass.Location()
    families = test_town.populate()

    for mem in families:
        s_network = LocationClass.SocialNetwork()
        s_network.populateAssociates(mem)
        all_families.append(s_network.families)

    # TODO: Help
    for NPC in test_town.citizens:
        for family in all_families:
            for member in family:
                for person in member:
                    if NPC.NPC_UUID is person.get_id():
                        NPC.NPC_Social_Network = family
                        break

    stop = datetime.now()
    time = stop - start

    r = random.randint(0, len(test_town.citizens))

    print(f"Location size: {test_town.size} \
          Time to create Location: {time} \
          Size of Location {utilities.getsize(test_town)} bytes")
    print(f"Randomly selected NPC: {test_town.citizens[r].NPC_UUID}")
    print(f"                       {test_town.citizens[r].NPC_Name}")


if __name__ == '__main__':
    # CSREI = testCSREI()
    # testOCEAN(CSREI)
    # testMakeNPC()

    makeLocation()
