import re

from .base_module import BaseModule
from nero.request import Request
from nero.utils import (
    uniform,
    get_path,
    longest_repeated_substring,
)


class DynamicPathDiscovery(BaseModule):

    def generate_request(self):
        random_path = self.dynamic_memory.get_one_random("path")
        if random_path == None:
            return None

        request = Request()
        request.method = uniform(["GET"])
        request.path = random_path
        request.cookies = self.dynamic_memory.get_random_full_cookies()

        return request
