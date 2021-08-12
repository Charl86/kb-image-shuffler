"""Unit test for Key class."""

import unittest
from shufflealgos.image.key import Key


class TestKey(unittest.TestCase):
    """TestCase class that will test Key class methods."""

    def test_shift_to_range(self):
        """Test shift_to_range method of a Key object."""
        absolute_minimum: int = 11
        absolute_maximum: int = 14
        curr_key: Key = Key(values=[4, 5, 6])
        shifted_key: Key = curr_key.shift_to_range(absolute_minimum,
                                                   absolute_maximum)

        self.assertEqual(shifted_key.values, [11, 12, 13])
        self.assertTrue(min(shifted_key.values) >= absolute_minimum)
        self.assertTrue(max(shifted_key.values) <= absolute_maximum)
        self.assertTrue(curr_key.length == shifted_key.length)

        absolute_minimum = 1
        absolute_maximum = 3
        curr_key = Key(values=[93, 68, 76, 88, 96, 93, 80])
        shifted_key = curr_key.shift_to_range(absolute_minimum,
                                              absolute_maximum)
        self.assertEqual(shifted_key.values, [3, 2, 1, 1, 3, 3, 2])
        self.assertTrue(min(shifted_key.values) >= absolute_minimum)
        self.assertTrue(max(shifted_key.values) <= absolute_maximum)
        self.assertTrue(curr_key.length == shifted_key.length)

        absolute_minimum = 12
        absolute_maximum = 19
        curr_key = Key(values=[20, 16, 13, 20, 16, 18, 20, 21, 17, 22])
        shifted_key = curr_key.shift_to_range(absolute_minimum,
                                              absolute_maximum)
        self.assertEqual(shifted_key.values,
                         [12, 16, 13, 12, 16, 18, 12, 13, 17, 14])
        self.assertTrue(min(shifted_key.values) >= absolute_minimum)
        self.assertTrue(max(shifted_key.values) <= absolute_maximum)

    def test_get_extended_key(self):
        """Test get_extended_key method of a Key object."""
        curr_key: Key = Key(values=[1, 2, 3])
        extended_key: Key = curr_key.get_extended_key(5)

        self.assertEqual(extended_key.values, [1, 2, 3, 2, 3])

        curr_key = Key(values=[19, 15, 12, 19, 15, 17, 19])
        extended_key = curr_key.get_extended_key(17)

        self.assertEqual(extended_key.values,
                         curr_key.values
                         + [12, 16, 13, 12, 16, 18, 12, 13, 17, 14])

        curr_key = Key(values=[3, 3, 2, 1])
        extended_key = curr_key.get_extended_key(10)
        self.assertEqual(extended_key.values,
                         curr_key.values + [1, 1, 3, 2, 2, 2])


if __name__ == "__main__":
    unittest.main()
