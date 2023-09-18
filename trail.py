from __future__ import annotations
from dataclasses import dataclass
from mountain import Mountain
from data_structures.linked_stack import LinkedStack
from typing import TYPE_CHECKING, Union
from personality_decision import PersonalityDecision
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
        
        current = self
        go_top = current.store.top
        go_bot = current.store.bottom
        following_stack = []

        while following_stack:
            
            '''Top/Bot/Lazy Walker--------------------------------------------------------------------------------------------------------------'''
             
            while isinstance(current, TrailSplit): #if current is TrailSplit
                following_stack.append(current.following) #add following to stack
                    
                if personality.select_branch(current.store.top, current.store.bottom) == PersonalityDecision.TOP: #if top walker
                    current = go_top # go to top branch of split
                    
                if personality.select_branch(current.store.top, current.store.bottom) == PersonalityDecision.BOTTOM: #if top walker
                    current = go_bot # go to top branch of split

            while isinstance(current, TrailSeries): #if Trailseries i.e straight line store mountain
                personality.add_mountain(current.mountain)
                    
                while isinstance(current.following, TrailSeries): #if first Trailseries has trail series as its follwing 
                    personality.add_mountain(current.following.mountain) # keep adding the mountain of the following which is another trailseries
                    current = current.following #go to its following, then rechecks if the following is a trailseries


                while isinstance(current.following, TrailSplit): # if another trail split after the first trail split
                    following_stack.append(current.following) # store the following of the split
                    
                    if personality.select_branch() == PersonalityDecision.TOP: #if top walker
                        current = current.store.top # go to top branch of split
                    
                    if personality.select_branch() == PersonalityDecision.BOTTOM: #if top walker
                        current = current.store.bottom # go to top branch of split
                        
            if isinstance(current.following, None): # if the following is None
                current =  following_stack.pop() # then pop the following from the stack because that whole split section is finished
            '''------------------------------------------------------------------------------------------------------------------------'''
       
        
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        return 

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        pass

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        pass

