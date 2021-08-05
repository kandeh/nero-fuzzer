from .base_module import BaseModule
from nero.request import Request
from nero.utils import uniform, get_path


class CookieSaver(BaseModule):

    def process_response(self, request, response):
        for cookie in response.cookies:
            self.dynamic_memory.add_cookie(cookie.name, cookie.value)
