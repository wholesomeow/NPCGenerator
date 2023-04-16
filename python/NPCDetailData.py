import random

from enum import Flag, Enum
from aenum import Enum as Aenum
from aenum import NoAlias


class NPCType(Flag):
    DEFAULT = 0
    MAIN = 1
    SIDE = 2
    IMPORTANT = 4
    RETURNING = 8
    ONEOFF = 16
    COMPANION = 32
    FRIEND = 64
    NEUTRAL = 128
    ENEMY = 256
    DEAD = 512


class SexType(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class OrientationType(Enum):
    ASEXUAL = 1
    AROMANTIC = 2
    STRAIGHT = 3
    DEMISEXUAL = 4
    GAY = 5
    BISEXUAL = 6
    PANSEXUAL = 7


class GenderType(Aenum):
    _settings_ = NoAlias

    AGENDER = 4
    BIGENDER = 3
    CISGENDER = 3
    GENDERFLUID = 7
    GENDERVARIANT = 4
    NONBINARY = 4
    TRANSGENDERMAN = 1
    TRANSGENDERWOMAN = 2


class BodyType(Enum):
    SINEWY = 5
    LEAN = 10
    BUFF = 15
    BUILT = 20
    THIN = 6
    AVERAGE = 12
    BIGGER = 18
    LARGE = 24
    REEDY = 7
    SOFT = 14
    PLUMP = 21
    FAT = 28


def generateBodyType(height, weight):
    meters = height / 100
    BMI = round((weight / meters**2), 2)

    # Selects a level of health for how the person treats their body
    # 5 = In shape, 6 = Average, 7 = Not in shape
    health_Level = random.randint(5, 7)

    if BMI <= 18.5:
        body_ID = 1
    elif 18.5 < BMI <= 24.9:
        body_ID = 2
    elif 25 < BMI <= 29.29:
        body_ID = 3
    else:
        body_ID = 4

    body_select = health_Level * body_ID
    return BodyType(body_select)
