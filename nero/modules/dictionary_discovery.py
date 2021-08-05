from .base_module import BaseModule
from nero.request import Request
from nero.utils import uniform


class DictionaryDiscovery(BaseModule):

    def generate_request(self):
        request = Request()

        request.method = uniform(["GET"])
        request.path = self.static_memory.get_one_random("path")
        request.cookies = self.dynamic_memory.get_random_full_cookies()

        return request
