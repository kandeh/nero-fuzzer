import unittest

from nero.modules import HTMLParamExtractor
from nero.memory import Memory
from nero.utils import empty_object


class TestHTMLParamExtractor(unittest.TestCase):

    def test_html_param_exract(self):
        with open("./tests/test_data/text4.html", "r") as file:
            text = file.read()
        
        dynamic_memory = Memory()
        module = HTMLParamExtractor(None, dynamic_memory)
        response = empty_object()
        response.text = text
        module.process_response(None, response)

        self.assertListEqual(
            sorted(list(dynamic_memory.data['param'])),
            sorted(["fname", "lname"])
        )
