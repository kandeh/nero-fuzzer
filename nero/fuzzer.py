import os
import urllib
import multiprocessing

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
    JsonAndYamlParamExtractor,
    HTMLParamExtractor,
    FrobiddenRetry,
)

HTTP_FUNCS = {
    "GET": requests.get,
    "POST": requests.post,
    "DELETE": requests.delete,
    "PATCH": requests.patch,
    "PUT": requests.put,
    "HEAD": requests.head,
    "OPTIONS": requests.options,
}

def send(request):
    url = f"{request.target}{request.path}"

    func = HTTP_FUNCS.get(request.method, None)
    data = {
        "headers": request.headers,
        "cookies": request.cookies,
    }

    data['headers']['Content-Type'] = request.content_type
    data['headers']['referer'] = request.target

    params = request.params

    if request.method == "GET":
        params = {**params, **request.data}
    elif request.content_type == "application/json":
        data["json"] = request.data
    else:
        data["data"] = request.data

    if request.params != {}:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    response = func(url,  allow_redirects=False, **data, verify=False, timeout=5)
    return response

class NeroFuzzer:
    N_PARALLEL = 4
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
        JsonAndYamlParamExtractor,
        HTMLParamExtractor,
        FrobiddenRetry,
    ]

    def __init__(self, target, static_memory, dynamic_memory, reports):
        self.target = target
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.reports = reports
        self.process_pool = multiprocessing.Pool(processes=self.N_PARALLEL)

        self.modules = []
        for module in self.MODULES:
            self.modules.append(module(static_memory, dynamic_memory))

        self.run()


    def get_reports(self, request, response):
        ret = {
            "method": request.method,
            "url": response.url,
            "params": request.params,
            "data": request.data,
            "cookies": request.cookies,
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
            requests = []
            for i in range(self.N_PARALLEL):
                request = self.generate_request()
                request.target = self.target
                requests.append(request)

            responses = self.process_pool.map(send, requests)

            for i in range(len(requests)):
                request = requests[i]
                response = responses[i]

                self.process_response(request, response)
                new_report = self.get_reports(request, response)
                if len(new_report['details']) > 0:
                    self.reports.append(new_report)
