import random
import copy

from .base_module import BaseModule
from nero.request import ALL_CONTENT_TYPES
from nero.data_producer import DataProducer
from nero.utils import uniform


class BadRequestRetry(BaseModule):

    def __init__(self, static_memory, dynamic_memory):
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.requests = []


    def mutate_content_type(self, request):
        ret = copy.copy(request)

        if random.random() > 0.5:
            return ret
        
        ret.content_type = uniform(ALL_CONTENT_TYPES, [request.content_type])
        return ret


    def mutate_data_and_params(self, request):
        ret = copy.copy(request)

        if random.random() > 0.5:
            return ret
        
        all_fields = []

        for pk in request.params.keys():
            all_fields.append((pk, request.params[pk]))

        for dk in request.params.keys():
            all_fields.append((dk, request.params[dk]))

        producer = DataProducer()
        producer.add_source(self.static_memory)
        producer.add_source(self.dynamic_memory)

        random.shuffle(all_fields)
        all_fields = all_fields[:100]

        for i in range(100):
            field_name = producer.get("param")
            field_value = producer.get(field_name)
            all_fields.append((field_name, field_value))
        
        n_params = random.randint(0, 100)
        n_data = random.randint(0, 100)

        ret.params = {}
        ret.data = {}

        for i in range(n_params):
            random_field = uniform(all_fields)
            ret.params[random_field[0]] = random_field[1]

        for i in range(n_data):
            random_field = uniform(all_fields)
            ret.data[random_field[0]] = random_field[1]


        return ret


    def generate_request(self):
        if len(self.requests) < 1:
            return None

        random.shuffle(self.requests)
        request = self.requests.pop()

        request = self.mutate_content_type(request)
        request = self.mutate_data_and_params(request)

        return request


    def process_response(self, request, response):
        if response.status_code == 400:
            self.requests.append(copy.copy(request))
