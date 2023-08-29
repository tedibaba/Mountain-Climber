import unittest
from ed_utils.decorators import number

from mountain import Mountain
from mountain_organiser import MountainOrganiser

class TestInfiniteHash(unittest.TestCase):

    @number("6.1")
    def test_example(self):
        m1 = Mountain("m1", 2, 2)
        m2 = Mountain("m2", 9, 2)
        m3 = Mountain("m3", 6, 3)
        m4 = Mountain("m4", 1, 3)
        m5 = Mountain("m5", 6, 4)
        m6 = Mountain("m6", 3, 7)
        m7 = Mountain("m7", 7, 7)
        m8 = Mountain("m8", 8, 7)
        m9 = Mountain("m9", 6, 7)
        m10 = Mountain("m10", 4, 8)

        mo = MountainOrganiser()
        mo.add_mountains([m1, m2])

        self.assertEqual([mo.cur_position(m) for m in [m1, m2]], [0, 1])
        mo.add_mountains([m4, m3])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
        mo.add_mountains([m5])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
        mo.add_mountains([m7, m9, m6, m8])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])

        self.assertRaises(KeyError, lambda: mo.cur_position(m10))
