from __future__ import annotations
from mountain import Mountain
from double_key_table import DoubleKeyTable

class MountainManager:

    def __init__(self) -> None:
        #We choose a double key table due to the assumed efficiency of O(1) for all its operations as well as being more logical over an infinite hash table as a data structure to store the mountains
        #It also makes it easier to get all the mountains grouped based on the difficulty level of the mountains
        self.mountains = DoubleKeyTable() 
        

    def add_mountain(self, mountain: Mountain) -> None:
        """
        The function adds a mountain object to a dictionary using its difficulty level and name as the
        key.
        
        :param mountain: The parameter "mountain" is of type Mountain
        """

        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain #We convert to a string so that the difficulty level can be hashed


    def remove_mountain(self, mountain: Mountain) -> None:
        """
        The function removes a mountain from a dictionary of mountains based on its difficulty level and
        name.
        
        :param mountain: The parameter "mountain" is of type Mountain
        
        :raises KeyError: If the mountain to delete does not exist
        """
        try:
            del self.mountains[str(mountain.difficulty_level), mountain.name]
        except KeyError:
            raise KeyError(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        The function `edit_mountain` deletes an old mountain object from a dictionary and adds a new
        mountain object to the same dictionary.
        
        :param old: The "old" parameter is an instance of the Mountain class that represents the
        mountain object that you want to edit or replace
        :param new: The "new" parameter is an instance of the Mountain class that represents the updated
        information for a mountain
        """
        del self.mountains[str(old.difficulty_level), old.name]
        self.mountains[str(new.difficulty_level), new.name] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        The function returns a list of mountains with a specified difficulty level.
        
        :param diff: The "diff" parameter is an integer that represents the difficulty level of the
        mountains
        :return: A list of mountains with a given difficulty level

        :complexity:
            :best case: O(n)
            :worst case: O(n)
            where n is the number of mountains with a given difficulty level
        """
        try:
            return self.mountains.values(str(diff))
        except KeyError:
            return []

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        The function `group_by_difficulty` groups mountains based on their difficulty level.
        :return: a list of lists of Mountain objects. Each inner list represents a group of mountains
        with the same difficulty level.
        :return: A list of lists containing mountains group according to their difficulty level

        :complexity:
            :best case: O(m)
            :worst case: O(m)
            where m is the number of mountains that have been added so far
        """
        mountain_groups = []
        difficulties = self.mountains.keys()
        for difficulty in difficulties:
            diff_mountains = self.mountains.values(difficulty)
            mountain_groups.append(diff_mountains)
        return mountain_groups
        
