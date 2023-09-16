from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

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
        return TrailSeries(self.following.store.mountain, Trail(None))


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
        if self.following == Trail(None):
            return None
        return TrailSeries(self.following.store.mountain, self.following.store.following)#EROROROROROROROROR

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
        return Trail(TrailSplit(Trail(None), Trail(None), Trail(self.store)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        pass

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        #Recursive style
        return self.aux_collect_all_mountains(self, [])
    
    def aux_collect_all_mountains(self, curr, mountains: list):
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
        pass

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.        
        paths = []
        min_max_path = [float("inf"), 0] #Kept in order as min, max
        #Need to consider a trail series being at the start
        # starting_path = self.traverse_trail_series(min_max_path, max_difference)

        return self.aux_difficulty_difference_paths([float("inf"), 0], [], paths, max_difference,0)


    def aux_difficulty_difference_paths(self, min_max_path, curr_path, paths, max_difference, top_or_bot): #curr_path is the accumulator

        if isinstance(self.store, TrailSplit):
            self.store.following.aux_difficulty_difference_paths(min_max_path, curr_path, paths, max_difference,0)

            self.store.top.aux_difficulty_difference_paths(min_max_path + [], curr_path + [], paths, max_difference, 1)

            self.store.bottom.aux_difficulty_difference_paths(min_max_path + [], curr_path + [], paths, max_difference, 1)


        elif isinstance(self.store, TrailSeries):
            curr_path +=  self.traverse_trail_series(min_max_path) 
            self.store.following.aux_difficulty_difference_paths(min_max_path, curr_path, paths, max_difference, top_or_bot)
        
        elif self == Trail(None) and top_or_bot:
            if min_max_path[1] - min_max_path[0] <= max_difference:
                paths.append(curr_path[::-1])
    
        return paths


    def traverse_trail_series(self, min_max_path):
        path_series = []
        curr = self
        if isinstance(curr.store, TrailSeries):
        #These mountains must be traversed
            while not isinstance(curr.store, TrailSplit):
                    path_series.append(curr.store.mountain)
                    min_max_path[0] = min(min_max_path[0], curr.store.mountain.difficulty_level)
                    min_max_path[1] = max(min_max_path[1], curr.store.mountain.difficulty_level)
                    if curr.store.following != Trail(None):
                        curr = curr.store.following
                    else:
                        return path_series
        return path_series

























# # 1054 ONLY!
# stack = LinkedStack() # We only want splits here 
# paths = []
# curr_path = []
# max_min_mountains_diff = [0 , 0] #Kept in order as min and max
# stack.push(self)
# while not stack.empty():
#     curr = stack.peek()
#     if isinstance(curr.store,TrailSplit):
#         #Traverse if not None
#         if curr.store.top != Trail(None):
            
#         if curr.store.bottom != Trail(None):
            
#         if curr.store.following != Trail(None):
            
#     if isinstance(curr.store, TrailSeries):
#         #We want to keep going through this series
#         curr_series_trail = curr.store
#         while curr_series_trail != Trail(None):
#             #If we exceed the diff given, we need to abandon the possible path
#             curr_path.append(curr_series_trail.mountain)
#             if curr_series_trail.mountain.difficulty_level > max_min_mountains_diff[1]:
#                 max_min_mountains_diff[1] = curr_series_trail.mountain.difficulty_level
#             elif curr_series_trail.mountain.difficulty_level < max_min_mountains_diff[0]:
#                 max_min_mountains_diff[0] = curr_series_trail.mountain.difficulty_level
#             if max_min_mountains_diff[1] - max_min_mountains_diff[0] > max_difference:
#                 #Abandon path
#                 curr_path.clear()


        # while not stack.empty():
        #     curr = stack.peek()
        #     if isinstance(curr, TrailSplit): #DO I NEED THIS?
        #         if curr.top != Trail(None):
        #             curr.top.traverse_trail_series()
        #         else:
        #             #Take the top without climbing anything


    # def aux_difficulty_difference_paths(self, paths, stack : LinkedStack, max_difference, min_max_path, curr_path: list[Mountain], curr_path1, tag, parent):
    #     if isinstance(self.store, TrailSplit):
    #         path = []
    #         path1 = []
    #         if self.store.top != Trail(None): #Even if its none, we can traverse it so we go to following

    #             # stack.push(self.store.top)
    #             path = self.store.top.aux_difficulty_difference_paths(paths, stack, max_difference, min_max_path, curr_path, curr_path1, 0, parent)
    #             curr_path += path


    #         curr_path.append(self.store.following.aux_difficulty_difference_paths(paths, stack, max_difference, min_max_path, curr_path + path, curr_path1, 0, parent))


    #         if self.store.bottom != Trail(None):

    #             path1 = self.store.bottom.aux_difficulty_difference_paths(paths, stack, max_difference, min_max_path, curr_path , curr_path1,1, parent)
    #             curr_path += path1

    #         curr_path1.append(self.store.following.aux_difficulty_difference_paths(paths, stack, max_difference, min_max_path, curr_path, curr_path1  + path1, 1, parent))

    #     elif isinstance(self.store, TrailSeries):
    #         return self.traverse_trail_series(min_max_path, max_difference)


    #     if self == parent:
    #         paths.append(curr_path)
    #         paths.append(curr_path1)
        
    #     if tag ==0:
    #         return curr_path
    #     else:
    #         return curr_path1
