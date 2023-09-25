from __future__ import annotations
from abc import ABC, abstractmethod
from enum import auto
from base_enum import BaseEnum
from mountain import Mountain
from trail import Trail
from personality_decision import PersonalityDecision
from trail import Trail,TrailSeries,TrailSplit

class WalkerPersonality(ABC):
    def __init__(self) -> None:
        self.mountains = []
        

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains.append(mountain)

    @abstractmethod
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
        pass

class TopWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
        # Always select the top branch
        return PersonalityDecision.TOP

class BottomWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
        # Always select the bottom branch
        return PersonalityDecision.BOTTOM

class LazyWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
        """
        Try looking into the first mountain on each branch,
        take the path of least difficulty.
        """

        # isinstance breaks across imports if running the original file as main
        # So just check __class__.__name__ :(
        top_m = top_branch.store.__class__.__name__ == "TrailSeries"
        bot_m = bottom_branch.store.__class__.__name__ == "TrailSeries"
        if top_m and bot_m:
            if top_branch.store.mountain.difficulty_level < bottom_branch.store.mountain.difficulty_level:
                return PersonalityDecision.TOP
            elif top_branch.store.mountain.difficulty_level > bottom_branch.store.mountain.difficulty_level:
                return PersonalityDecision.BOTTOM
            return PersonalityDecision.STOP
        # If one of them has a mountain, don't take it.
        # If neither do, then take the top branch.
        if top_m:
            return PersonalityDecision.BOTTOM
        return PersonalityDecision.TOP

# if __name__ == "__main__":

#     def load_example(self):
#         self.top_top = Mountain("top-top", 5, 3)
#         self.top_bot = Mountain("top-bot", 3, 5)
#         self.top_mid = Mountain("top-mid", 4, 7)
#         self.bot_one = Mountain("bot-one", 2, 5)
#         self.bot_two = Mountain("bot-two", 0, 0)
#         self.final   = Mountain("final", 4, 4)
#         self.trail = Trail(TrailSplit(
#             Trail(TrailSplit(
#                 Trail(TrailSeries(self.top_top, Trail(None))),
#                 Trail(TrailSeries(self.top_bot, Trail(None))),
#                 Trail(TrailSeries(self.top_mid, Trail(None))),
#             )),
#             Trail(TrailSeries(self.bot_one, Trail(TrailSplit(
#                 Trail(TrailSeries(self.bot_two, Trail(None))),
#                 Trail(None),
#                 Trail(None),
#             )))),
#             Trail(TrailSeries(self.final, Trail(None)))
#         ))

#     def test_example(self):
#         example = load_example()
#         example.load_example()
#         tw = TopWalker()
#         bw = BottomWalker()
#         lw = LazyWalker()
#         example.trail.follow_path(tw)
#         example.trail.follow_path(bw)
#         example.trail.follow_path(lw)

#         # self.assertListEqual(tw.mountains, [self.top_top, self.top_mid, self.final])
#         # self.assertListEqual(bw.mountains, [self.bot_one, self.final])
#         # self.assertListEqual(lw.mountains, [self.top_bot, self.top_mid, self.final])
