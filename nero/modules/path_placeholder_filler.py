import re

from .base_module import BaseModule
from nero.request import Request
from nero.utils import uniform, get_path
from nero.data_producer import DataProducer


class PathPlaceholderFiller(BaseModule):

    def generate_request(self):
        all_candidates = []

        for path in self.dynamic_memory.data.get('path', set()):
            matches = re.findall(r"{[\.a-zA-Z0-9:]+}", path)
            if len(matches) > 0:
                all_candidates.append(path)

        path = uniform(all_candidates)

        if path == None:
            return None

        producer = DataProducer()
        producer.add_source(self.static_memory)
        producer.add_source(self.dynamic_memory)

        matches = re.findall(r"{[\.a-zA-Z0-9:]+}", path)
        while len(matches) > 0:
            for place in matches:
                path = path.replace(place, producer.get(place[1:-1]), 1)
            matches = re.findall(r"{[\.a-zA-Z0-9:]+}", path)
        
        request = Request()
        request.method = uniform(["GET", "POST", "DELETE"])
        request.path = path
        request.cookies = self.dynamic_memory.get_random_full_cookies()
        return request
