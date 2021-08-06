import unittest

from nero.utils import uniform


class TestUtils(unittest.TestCase):

    def test_uniform(self):
        for i in range(1000):
            arr = [0, 1, 2, 3]
            exclude = [0, 2]
            random_element = uniform(arr, exclude)
            self.assertIn(random_element, [1, 3])
