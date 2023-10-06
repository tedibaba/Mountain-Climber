import unittest
from ed_utils.decorators import number, advanced

from mountain import Mountain
from trail import Trail, TrailSeries, TrailSplit

class TestTrailMethods(unittest.TestCase):

    def load_example(self):
        self.top_top = Mountain("top-top", 6, 3)
        self.top_bot = Mountain("top-bot", 3, 5)
        self.top_mid = Mountain("top-mid", 7, 2)
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
                Trail(TrailSplit(Trail(None), Trail(None), Trail(None))),
                Trail(None),
            )))),
            Trail(TrailSeries(self.final, Trail(None)))
        ))

    @number("7.1")
    def test_collect_all_mountains(self):
        self.load_example()
        res = self.trail.collect_all_mountains()

        hash_mountain = lambda m: m.name

        self.assertEqual(len(res), 6)
        self.assertSetEqual(set(map(hash_mountain, res)), set(map(hash_mountain, [
            self.top_bot, self.top_top, self.top_mid,
            self.bot_one, self.bot_two, self.final
        ])))

    # @number("7.2")
    # def test_difficulty_maximum_paths(self):
    #     self.load_example()

    #     res = self.trail.difficulty_maximum_paths(5)
    #     make_path_string = lambda mountain_list: ", ".join(map(lambda x: x.name, mountain_list))
    #     # This makes the result a list of strings, like so:
    #     # [
    #     #   "top-bot, top-middle, final",
    #     #   "bot-one, final"
    #     # ]
    #     res = list(map(make_path_string, res))
    #     res.sort()

    #     expected_res = [
    #         "bot-one, final",
    #         "bot-one, final", # twice because of the empty split.
    #         "bot-one, bot-two, final",
    #     ]
    #     expected_res.sort()

    #     self.assertListEqual(res, expected_res)

    @number("7.3")
    def test_difficulty_difference_paths(self):
        self.load_example()

        res = self.trail.difficulty_difference_paths(3)
        make_path_string = lambda mountain_list: ", ".join(map(lambda x: x.name, mountain_list))
        # This makes the result a list of strings, like so:
        # [
        #   "top-bot, top-middle, final",
        #   "bot-one, final"
        # ]
        res = list(map(make_path_string, res))
        res.sort()

        expected_res = [
            "top-top, top-mid, final",
            "bot-one, final",
            "bot-one, final", # twice because of the empty split.
        ]
        expected_res.sort()

        self.assertListEqual(res, expected_res)

    @number("7.4")
 
    def test_difficulty_difference_paths_simple(self):
        m1 = Mountain("m1", 0, 1)
        m2 = Mountain("m2", 2, 1)
        m3 = Mountain("m3", 4, 1)
        m4 = Mountain("m4", 6, 1)
        m5 = Mountain("m5", 8, 1)

        trail = Trail(TrailSeries(m1, Trail(TrailSeries(m2, Trail(TrailSeries(
            m3, Trail(TrailSeries(m4, Trail(TrailSeries(m5, Trail(None)))))))))))
        res = trail.difficulty_difference_paths(3)

        def make_path_string(mountain_list): return ", ".join(
            map(lambda x: x.name, mountain_list))

        res = list(map(make_path_string, res))
        res.sort()

        expected_res = [
            "m1, m2, m3, m4, m5",
        ]
        expected_res.sort()

        self.assertListEqual(res, expected_res)
    
