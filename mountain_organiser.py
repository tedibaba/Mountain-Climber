from __future__ import annotations

from mountain import Mountain
from algorithms.binary_search import binary_search
from algorithms.mergesort import merge, mergesort

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountain_ranks = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        The function `cur_position` returns the position of a given mountain in a list of mountain ranks
        using binary search.
        
        :param mountain: The parameter "mountain" is of type "Mountain". It represents the mountain
        object for which we want to find the current position
        :return: the position of the mountain in the list `self.mountain_ranks`.

        :complexity:
            :best case: O(log(n))
            :worst case: O(log(n))
            where n is the number of mountains in the organiser so far
        """
        
        pos = binary_search(self.mountain_ranks, mountain)
        if self.mountain_ranks[pos] == mountain:
            return pos
        else:
            raise KeyError(mountain)
         
    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        The function `add_mountains` takes a list of mountains and inserts them into a sorted list of
        mountain ranks using binary search.
        
        :param mountains: A list of Mountain objects that you want to add to the existing list of
        mountain ranks
        
        :complexity:
            :best case: O(mlog(n))
            :worst case: O(mlog(m) + n)
            where n is the number of mountains in the organiser so far, m is the number of mountains to be added
        """
        mountains = mergesort(mountains)
        self.mountain_ranks = merge(mountains, self.mountain_ranks)
