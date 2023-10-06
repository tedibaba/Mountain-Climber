from __future__ import annotations
from dataclasses import dataclass
from mountain import Mountain
from data_structures.linked_stack import LinkedStack
from typing import TYPE_CHECKING, Union

from data_structures.linked_stack import LinkedStack

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.following.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """
       
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        return TrailSeries(mountain, Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
 
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, Trail(self))))

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality.
        
        :param personality: A personality that dictates what path on the trail will be followed

        :complexity:
            :best case: O(n)
            :worst case: O(n)
            where n is the number of mountains that are to be followed
        """

        stack  = LinkedStack() #Only trail splits be in the stack
        if isinstance(self.store, TrailSeries): #If there is a trail series at the start, then we traverse through it until we reach the a trail split
            self.traverse_series_path(self, stack, personality)
        elif isinstance(self.store, TrailSplit):
            stack.push([self, 0]) 
        while not stack.is_empty():
            branch, seen = stack.peek() if stack.peek()[1] == 0 else stack.pop()
            path = personality.select_branch(branch.store.top, branch.store.bottom).value
            if path == 3:
                break #Stop the traversal

            if not seen:
                stack.peek()[1] = 1
                if path == 1:
                    if isinstance(branch.store.top.store, TrailSeries):
                        self.traverse_series_path(branch.store.top, stack, personality)
                       
                    elif isinstance(branch.store.top.store, TrailSplit):
                        stack.push([branch.store.top, 0])

                elif path == 2:
                    if isinstance(branch.store.bottom.store, TrailSeries):
                        self.traverse_series_path(branch.store.bottom, stack, personality)

                    elif isinstance(branch.store.bottom.store, TrailSplit):
                        stack.push([branch.store.bottom, 0])
               
            else:
                if branch.store.following != Trail(None): #If we have seen this trailSplit already, we would have already traversed either the top or bottom branch we want to and hence we can traverse the following part of the trail split.
                    personality.add_mountain(branch.store.following.store.mountain)


    def traverse_series_path(self, curr, stack, personality):
        #The while loop traverses through every mountain in series
        while curr != Trail(None):
            personality.add_mountain(curr.store.mountain)
            if isinstance(curr.store.following.store, TrailSplit):
                stack.push([curr.store.following, 0])
                break
            curr = curr.store.following


    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        #Recursive style
        return self.aux_collect_all_mountains(self, [])
    
    def aux_collect_all_mountains(self, curr, mountains: list):
        """
        The function `aux_collect_all_mountains` recursively collects all the mountains from a given
        trail structure.
        
        :param curr: The variable `curr` represents the current node in a trail data structure. It is
        used to traverse the trail and collect information about mountains
        :param mountains: The `mountains` parameter is a list that is used to store the names of all the
        mountains encountered during the traversal of a trail
        :return: a list of all the mountains encountered while traversing the trail.
        """
        if isinstance(curr.store, TrailSeries):
            mountains.append(curr.store.mountain)
            if curr.store.following != Trail(None):
                return self.aux_collect_all_mountains(curr.store.following, mountains)
        elif isinstance(curr.store,TrailSplit):
            if curr.store.top != Trail(None):
                self.aux_collect_all_mountains(curr.store.top, mountains)
            if curr.store.bottom != Trail(None):
                self.aux_collect_all_mountains(curr.store.bottom, mountains)
            if curr.store.following != Trail(None):
                self.aux_collect_all_mountains(curr.store.following, mountains)
            
        #Base case when reached the end of the trail
        return mountains
             

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        paths = self.collect_all_paths([])
        path = [path for path in paths if max([mountain.difficulty_level for mountain in path]) <= max_difficulty]
        return path

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.        
        res = []
        
        paths = self.collect_all_paths([])
        for path in paths:
            # min_max_path = [float("inf"), 0] #Kept in order as min, max
            for i in range(len(path) - 1):
                # min_max_path[0] = min(min_max_path[0], mountain.difficulty_level)
                # min_max_path[1] = max(min_max_path[1], mountain.difficulty_level)
                # if min_max_path[1] - min_max_path[0] <= max_difference:
                #     res.append(path)
                if abs(path[i + 1].difficulty_level - path[i].difficulty_level) > max_difference:
                    break
            else:
                res.append(path)
        return res
    

    def collect_all_paths(self, res):
        if isinstance(self.store, TrailSplit):
            top, bottom, following = self.store.top.collect_all_paths([]), self.store.bottom.collect_all_paths([]), self.store.following.collect_all_paths([])
            top.extend(bottom) #All top paths and bottom paths should be followed by the following path
            for path in following:
                for branch in top:
                    res.append(branch + path)
            return res

        elif isinstance(self.store, TrailSeries):
            following = self.store.following.collect_all_paths([])
            for path in following:
                res.append([self.store.mountain] + path)

            return res

        elif self == Trail(None):
            return [[]]
 
