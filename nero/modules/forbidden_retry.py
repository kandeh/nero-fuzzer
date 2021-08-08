import random
import copy

from .base_module import BaseModule
from nero.data_producer import DataProducer
from nero.utils import uniform


class FrobiddenRetry(BaseModule):

    def __init__(self, static_memory, dynamic_memory):
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.requests = []


    def set_cookies(self, request):
        if request.cookies == {} or random.random() < 0.5:
            request.cookies = self.dynamic_memory.get_random_full_cookies()


    def set_csrf_headers(self, request):
        csrf_tokens = set()

        for cookie_name in request.cookies.keys():
            if "csrf" in cookie_name.lower():
                csrf_tokens.add(request.cookies[cookie_name])

        if len(csrf_tokens) == 0:
            return

        csrf_headers = list(self.static_memory.data['csrf_header'])
        random.shuffle(csrf_headers)

        for csrf_header in csrf_headers[:3]:
            request.headers[csrf_header] = uniform(csrf_tokens)


    # TODO:
    def set_auth_headers(self, request):
        pass


    def generate_request(self):
        if len(self.requests) < 1:
            return None

        random.shuffle(self.requests)
        request = self.requests.pop()

        self.set_cookies(request)
        self.set_csrf_headers(request)
        self.set_auth_headers(request)

        return request


    def process_response(self, request, response):
        if response.status_code in [401, 403]:
            self.requests.append(copy.copy(request))
