import unittest

from nero.modules import JsonAndYamlParamExtractor
from nero.memory import Memory
from nero.utils import empty_object


class TestJsonAndYamlParamExtractor(unittest.TestCase):

    def test_yaml_param_exract(self):
        with open("./tests/test_data/text2.yml", "r") as file:
            text = file.read()
        
        dynamic_memory = Memory()
        module = JsonAndYamlParamExtractor(None, dynamic_memory)
        response = empty_object()
        response.text = text
        module.process_response(None, response)

        self.assertListEqual(
            sorted(list(dynamic_memory.data['param'])),
            sorted(['0', '___', 'email', 'name', 'test'])
        )


    def test_json_param_exract(self):
        with open("./tests/test_data/text3.json", "r") as file:
            text = file.read()
        
        dynamic_memory = Memory()
        module = JsonAndYamlParamExtractor(None, dynamic_memory)
        response = empty_object()
        response.text = text
        module.process_response(None, response)

        self.assertListEqual(
            sorted(list(dynamic_memory.data['param'])),
            sorted(['0', '___', 'name', 'test', "is", "not", "valid", "details"])
        )

    def test_non_json_and_yaml_dont_extract_params(self):
        with open("./tests/test_data/text.txt", "r") as file:
            text = file.read()
        
        dynamic_memory = Memory()
        module = JsonAndYamlParamExtractor(None, dynamic_memory)
        response = empty_object()
        response.text = text
        module.process_response(None, response)

        self.assertListEqual(
            sorted(list(dynamic_memory.data.get("param", []))),
            []
        )
