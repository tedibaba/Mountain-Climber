from __future__ import annotations
from mountain import Mountain
from double_key_table import DoubleKeyTable

class MountainManager:

    def __init__(self) -> None:
        #We choose a double key table due to the assumed efficiency of O(1) for all its operations as well as being more logical over an infinite hash table as a data structure to store the mountains
        #It also makes it easier to get all the mountains grouped based on the difficulty level of the mountains
        self.mountains = DoubleKeyTable() 
        

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain #We convert to a string so that the difficulty level can be hashed


    def remove_mountain(self, mountain: Mountain) -> None:
        try:
            del self.mountains[str(mountain.difficulty_level), mountain.name]
        except KeyError:
            raise KeyError(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        del self.mountains[str(old.difficulty_level), old.name]
        self.mountains[str(new.difficulty_level), new.name] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        try:
            return self.mountains.values(str(diff))
        except KeyError:
            return []

    def group_by_difficulty(self) -> list[list[Mountain]]:
        mountain_groups = []
        difficulties = self.mountains.keys()
        for difficulty in difficulties:
            diff_mountains = self.mountains.values(difficulty)
            mountain_groups.append(diff_mountains)
        return mountain_groups
        
