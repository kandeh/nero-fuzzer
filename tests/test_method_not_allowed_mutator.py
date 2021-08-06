import unittest

from nero.modules import MethodNotAllowedMutator
from nero.memory import Memory
from nero.request import All_METHODS
from nero.utils import empty_object


class TestMethodNotAllowedMutator(unittest.TestCase):

    def test_method_not_allowd_should_mutate(self):
        module = MethodNotAllowedMutator(None, None)

        request = empty_object()
        request.method = All_METHODS[0]

        response = empty_object()
        response.status_code = 405 # method not allowed

        module.process_response(request, response)

        new_request = module.generate_request()

        self.assertNotEqual(new_request.method, request.method)
        self.assertIn(new_request.method, All_METHODS)


    def test_method_not_allowd_should_not_mutate(self):
        module = MethodNotAllowedMutator(None, None)

        request = empty_object()
        request.method = All_METHODS[0]

        response = empty_object()
        response.status_code = 200

        module.process_response(request, response)

        new_request = module.generate_request()

        self.assertEqual(new_request, None)
