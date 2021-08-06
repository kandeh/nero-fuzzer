import random
import copy

from .base_module import BaseModule
from nero.request import All_METHODS
from nero.utils import (
    uniform
)


class MethodNotAllowedMutator(BaseModule):

    def __init__(self, static_memory, dynamic_memory):
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.requests = []


    def generate_request(self):
        if len(self.requests) < 1:
            return None

        random.shuffle(self.requests)
        request = self.requests.pop()
        request.method = uniform(All_METHODS, [request.method])

        return request


    def process_response(self, request, response):
        if response.status_code == 405:
            self.requests.append(copy.copy(request))
