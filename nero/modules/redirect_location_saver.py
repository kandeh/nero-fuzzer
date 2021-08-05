from .base_module import BaseModule
from nero.request import Request
from nero.utils import uniform, get_path


class RedirectLocationSaver(BaseModule):

    def process_response(self, request, response):
        if "Location" in response.headers:
            self.dynamic_memory.add_one("path", get_path(response.headers['Location']))
