from __future__ import annotations
from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        #We choose a double key table due to the assumed efficiency of O(1) for all its operations as well as being more logical over an infinite hash table as a data structure to store the mountains
        #It also makes it easier to get all the mountains grouped based on the difficulty level of the mountains
        self.mountains = DoubleKeyTable() 
        

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain #We convert to a string so that the difficulty level can be hashed


    def remove_mountain(self, mountain: Mountain) -> None:
        raise NotImplementedError()

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        del self.mountains[str(old.difficulty_level), old.name]
        self.mountains[str(new.difficulty_level), new.name] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        raise NotImplementedError()

    def group_by_difficulty(self) -> list[list[Mountain]]:
        raise NotImplementedError()
