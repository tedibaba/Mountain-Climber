from base_enum import BaseEnum
from enum import auto
from mountain import Mountain
from abc import ABC, abstractmethod
# from trail import Trail

class PersonalityDecision(BaseEnum):
    TOP = auto()
    BOTTOM = auto()
    STOP = auto()