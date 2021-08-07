import unittest

from nero.utils import uniform, get_path


class TestUtils(unittest.TestCase):

    def test_uniform(self):
        for i in range(1000):
            arr = [0, 1, 2, 3]
            exclude = [0, 2]
            random_element = uniform(arr, exclude)
            self.assertIn(random_element, [1, 3])


    def test_get_path(self):
        tcs = [
            "/test/path?test",
            "http://127.0.0.1:8000/test/path?q=1&y=0",
            "http://127.0.0.1:8000/test/path",
            "http://test.com:8000/test/path",
            "http://test.com/test/path",
            "https://test.com/test/path",
            "test/path",
            "./test/path",
            "../../test/path",
        ]

        for tc in tcs:
            self.assertEqual(get_path(tc), "/test/path")

        self.assertEqual(None, None)
