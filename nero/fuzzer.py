import os

import requests

from .utils import load_data, uniform
from .memory import Memory

from .modules import (
    DictionaryDiscovery,
    DynamicPathDiscovery,
    RedirectLocationSaver,
    HTMLFormChecker,
    CookieSaver,
    PathPlaceholderFiller,
    ServerErrorReporter,
    YAMLBodyExtractor,
    RawBodyExtractor,
)


class NeroFuzzer:

    MODULES = [
        DictionaryDiscovery,
        DynamicPathDiscovery,
        RedirectLocationSaver,
        HTMLFormChecker,
        CookieSaver,
        PathPlaceholderFiller,
        ServerErrorReporter,
        YAMLBodyExtractor,
        RawBodyExtractor,
    ]

    def __init__(self, target, static_memory, dynamic_memory, reports):
        self.target = target
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.reports = reports

        self.modules = []
        for module in self.MODULES:
            self.modules.append(module(static_memory, dynamic_memory))

        self.run()


    def get_reports(self, request, response):
        ret = {
            "url": response.url,
            "method": request.method,
            "status_code": response.status_code,
            "details": [],
        }
        for module in self.modules:
            report = module.get_report(request, response)
            if report != None:
                ret['details'].append(report)
        return ret


    def generate_request(self):
        req = None
        while req == None:
            random_module = uniform(self.modules)
            req = random_module.generate_request()
        return req


    def process_response(self, request, response):
        for module in self.modules:
            module.process_response(request, response)


    def run(self):
        while True:
            request = self.generate_request()

            url = f"{self.target}{request.path}"
            
            func = None

            if request.method == "GET":
                func = requests.get

            if request.method == "POST":
                func = requests.post

            if request.method == "DELETE":
                func = requests.delete

            data = {
                "data": request.data,
                "headers": request.headers,
                "cookies": request.cookies,
            }

            response = func(url,  allow_redirects=False, **data)

            self.process_response(url, response)

            new_report = self.get_reports(request, response)
            if len(new_report['details']) > 0:
                self.reports.append(new_report)
