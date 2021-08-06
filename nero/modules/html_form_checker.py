import random

import lxml.html

from .base_module import BaseModule
from nero.request import Request
from nero.utils import uniform, get_path
from nero.data_producer import DataProducer


class HTMLFormChecker(BaseModule):

    def __init__(self, static_memory, dynamic_memory):
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.forms = []


    def generate_request(self):
        if len(self.forms) < 1:
            return None

        random.shuffle(self.forms)
        form = self.forms.pop()

        request = Request()
        request.method = form['method']
        request.path = form['url']
        request.cookies = {**self.dynamic_memory.get_random_full_cookies(), **form['cookies']}

        data = {}
        for hidden_input in form['hidden_inputs']: 
            data[hidden_input[0]] = hidden_input[1]

        producer = DataProducer()
        producer.add_source(self.static_memory)
        producer.add_source(self.dynamic_memory)

        for form_input in form['inputs']:
            data[form_input[0]] = producer.get(form_input[0])

        request.data = data

        return request


    def process_response(self, request, response):
        if len(response.text) < 1:
            return

        doc = lxml.html.fromstring(response.text.encode())

        forms = doc.xpath("//form")
        for form in forms:
            data = {
                "method": form.method,
                "action": form.action,
                "url": get_path(response.url),
                "hidden_inputs": [],
                "inputs": [],
                "cookies": {},
            }

            if data['action'] != None:
                data['url'] = data['url'] + data['action']

            for co in response.cookies:
                data['cookies'][co.name] = co.value

            for inp in form.xpath("//input"):
                if inp.type == "hidden":
                    data["hidden_inputs"].append([inp.name, inp.value])
                if inp.type in ["text", "password"]:
                    data["inputs"].append([inp.name, None])

            self.forms.append(data)
