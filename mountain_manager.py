from __future__ import annotations
from mountain import Mountain
from double_key_table import DoubleKeyTable

class MountainManager:

    def __init__(self) -> None:
        self.mountains = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain


    def remove_mountain(self, mountain: Mountain) -> None:
        try:
            del self.mountains[str(mountain.difficulty_level), mountain.name]
        except KeyError:
            raise KeyError(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        del self.mountains[old.difficulty_level, old.name]
        self.mountains[new.difficulty_level, new.name] = new

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
        
