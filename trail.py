from __future__ import annotations
from dataclasses import dataclass
from mountain import Mountain
from data_structures.stack_adt import Stack
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
        return TrailSeries(self.following, Trail(None))

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
        

        while self.store.top is not TrailSeries:
            if personality.select_branch(current.store.top, current.store.bottom) == PersonalityDecision.TOP:
                current = go_top
                personality.add_mountain(current.store.mountain)

            elif personality.select_branch(current.store.top, current.store.bottom) == PersonalityDecision.BOTTOM:
                current = go_bot
                personality.add_mountain(current.store.mountain)
       
            

            
        
    
            


    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        return 

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        pass

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        pass

