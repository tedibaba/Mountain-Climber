from __future__ import annotations

from mountain import Mountain
from algorithms.binary_search import binary_search

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountain_ranks = []

    def cur_position(self, mountain: Mountain) -> int:
        pos = binary_search(self.mountain_ranks, mountain)
        if self.mountain_ranks[pos] == mountain:
            return pos
        else:
            raise KeyError(mountain)
         
    def add_mountains(self, mountains: list[Mountain]) -> None:
        for mountain in mountains:
            pos = binary_search(self.mountain_ranks, mountain)
            self.mountain_ranks.insert(pos, mountain)

