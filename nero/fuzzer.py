import os
import urllib

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
    MethodNotAllowedMutator,
    BadRequestRetry,
)


class NeroFuzzer:
    HTTP_FUNCS = {
        "GET": requests.get,
        "POST": requests.post,
        "DELETE": requests.delete,
        "PATCH": requests.patch,
        "PUT": requests.put,
        "HEAD": requests.head,
        "OPTIONS": requests.options,
    }
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
        MethodNotAllowedMutator,
        BadRequestRetry,
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

            if request.params != {}:
                url = f"{url}?{urllib.parse.urlencode(request.params)}"

            func = self.HTTP_FUNCS.get(request.method, None)
            data = {
                "headers": request.headers,
                "cookies": request.cookies,
            }

            data['headers']['Content-Type'] = request.content_type

            if request.content_type == "application/json":
                data["json"] = request.data
            else:
                data["data"] = request.data

            response = func(url,  allow_redirects=False, **data)

            self.process_response(request, response)

            new_report = self.get_reports(request, response)
            if len(new_report['details']) > 0:
                self.reports.append(new_report)
