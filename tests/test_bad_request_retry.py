import unittest

from nero.modules import BadRequestRetry
from nero.memory import Memory
from nero.request import ALL_CONTENT_TYPES
from nero.utils import empty_object


class TestBadRequestRetry(unittest.TestCase):

    def setUp(self):
        self.module = BadRequestRetry(None, None)

        self.request = empty_object()
        self.request.method = "POST"
        self.request.content_type = ALL_CONTENT_TYPES[0]
        self.request.params = {"action": "search"}
        self.request.data = {"search": "book"}
        self.request.path = "/do"

        self.response = empty_object()
        self.response.status_code = 400 # bad request


    def test_bad_request_should_retry_with_different_content_type(self):
        old_requests_str = ""
        new_requests_str = ""
        for i in range(50):
            self.module.process_response(self.request, self.response)
            new_request = self.module.generate_request()

            old_requests_str = f"{old_requests_str}_{self.request.content_type}"
            new_requests_str = f"{new_requests_str}_{new_request.content_type}"

        self.assertNotEqual(new_requests_str, old_requests_str)


    def test_bad_request_should_retry_with_different_params(self):
        old_requests_str = ""
        new_requests_str = ""
        for i in range(50):
            self.module.process_response(self.request, self.response)
            new_request = self.module.generate_request()

            old_requests_str = f"{old_requests_str}_{self.request.params}"
            new_requests_str = f"{new_requests_str}_{new_request.params}"

        self.assertNotEqual(new_requests_str, old_requests_str)


    def test_bad_request_should_retry_with_different_data(self):
        old_requests_str = ""
        new_requests_str = ""
        for i in range(50):
            self.module.process_response(self.request, self.response)
            new_request = self.module.generate_request()

            old_requests_str = f"{old_requests_str}_{self.request.data}"
            new_requests_str = f"{new_requests_str}_{new_request.data}"

        self.assertNotEqual(new_requests_str, old_requests_str)


    def test_bad_request_should_not_retry(self):
        self.response.status_code = 200
        self.module.process_response(self.request, self.response)
        new_request = self.module.generate_request()
        self.assertEqual(new_request, None)


    def test_bad_request_should_not_change_path_and_method(self):
        for i in range(100):
            self.module.process_response(self.request, self.response)
            new_request = self.module.generate_request()

            self.assertEqual(new_request.method, self.request.method)
            self.assertEqual(new_request.path, self.request.path)
