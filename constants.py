from enum import auto
from base_enum import BaseEnum

class DrawMode(BaseEnum):
    EDIT = auto()
    ADD_MOUNTAIN = auto()
    ADD_BRANCH = auto()
    REMOVE = auto()
