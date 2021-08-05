import unittest

from nero.modules import RawBodyExtractor
from nero.memory import Memory
from nero.utils import empty_object


class TestRawBodyExtractor(unittest.TestCase):

    def test_upper(self):
        with open("./tests/test_data/text.txt", "r") as file:
            text = file.read()
        
        dynamic_memory = Memory()
        module = RawBodyExtractor(None, dynamic_memory)
        response = empty_object()
        response.text = text
        module.process_response(None, response)

        self.assertListEqual(
            sorted(list(dynamic_memory.data['email'])),
            sorted(['test2@test.test', 'test3@test.test', 'test@test.test'])
        )

        self.assertListEqual(
            sorted(list(dynamic_memory.data['path'])),
            sorted([
                "/path1/path2.php",
                "/file1.html",
                "/api/v1/",
                "/این یک مسیر است/search.asp"
                
                # TODO:
                # "/file2.rss",
            ])
        )

        self.assertListEqual(
            sorted(list(dynamic_memory.data['uuid'])),
            sorted([
                "4b377996-f5d0-11eb-9a03-0242ac130003",
                "5afa38ce-1330-4860-9b03-dfb752dee13b"

                # TODO:
                # "dd5219332a114b06b96bb3be93ca981f", 
            ])
        )
