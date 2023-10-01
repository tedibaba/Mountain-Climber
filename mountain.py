from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __lt__(self, mountain):
        if self.difficulty_level < mountain.difficulty_level:
            return True
        elif self.difficulty_level > mountain.difficulty_level:
            return False
        elif self.name < mountain.name:
            return True
        else:
            return False
        
    def __gt__(self, mountain):
        if self.difficulty_level > mountain.difficulty_level:
            return True
        elif self.difficulty_level < mountain.difficulty_level:
            return False
        elif self.name > mountain.name:
            return True
        else:
            return False

    def __le__(self, mountain):
        if self.difficulty_level < mountain.difficulty_level:
            return True
        elif self.difficulty_level > mountain.difficulty_level:
            return False
        elif self.name < mountain.name:
            return True
        else:
            return False
        
    def __ge__(self, mountain):
        if self.difficulty_level > mountain.difficulty_level:
            return True
        elif self.difficulty_level < mountain.difficulty_level:
            return False
        elif self.name > mountain.name:
            return True
        else:
            return False

