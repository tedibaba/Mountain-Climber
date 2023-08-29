import unittest
from ed_utils.decorators import number

from mountain import Mountain
from trail import Trail, TrailSeries, TrailSplit, TrailStore
from personality import WalkerPersonality, TopWalker, BottomWalker, LazyWalker, PersonalityDecision

class TestTrailMethods(unittest.TestCase):

    def load_example(self):
        self.top_top = Mountain("top-top", 5, 3)
        self.top_bot = Mountain("top-bot", 3, 5)
        self.top_mid = Mountain("top-mid", 4, 7)
        self.bot_one = Mountain("bot-one", 2, 5)
        self.bot_two = Mountain("bot-two", 0, 0)
        self.final   = Mountain("final", 4, 4)
        self.trail = Trail(TrailSplit(
            Trail(TrailSplit(
                Trail(TrailSeries(self.top_top, Trail(None))),
                Trail(TrailSeries(self.top_bot, Trail(None))),
                Trail(TrailSeries(self.top_mid, Trail(None))),
            )),
            Trail(TrailSeries(self.bot_one, Trail(TrailSplit(
                Trail(TrailSeries(self.bot_two, Trail(None))),
                Trail(None),
                Trail(None),
            )))),
            Trail(TrailSeries(self.final, Trail(None)))
        ))

    @number("2.1")
    def test_example(self):
        self.load_example()
        tw = TopWalker()
        bw = BottomWalker()
        lw = LazyWalker()
        self.trail.follow_path(tw)
        self.trail.follow_path(bw)
        self.trail.follow_path(lw)

        self.assertListEqual(tw.mountains, [self.top_top, self.top_mid, self.final])
        self.assertListEqual(bw.mountains, [self.bot_one, self.final])
        self.assertListEqual(lw.mountains, [self.top_bot, self.top_mid, self.final])


    @number("2.2")
    def test_custom_walk(self):
        class CustomWalker(WalkerPersonality):
            def __init__(self) -> None:
                super().__init__()
                self.count = 0
                self.choices = [PersonalityDecision.BOTTOM, PersonalityDecision.STOP]
            def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
                self.count += 1
                return self.choices[self.count - 1]

        self.load_example()
        cw = CustomWalker()
        self.trail.follow_path(cw)

        self.assertListEqual(cw.mountains, [self.bot_one])
