from .base_module import BaseModule
from nero.request import Request
from nero.utils import uniform, get_path


class ServerErrorReporter(BaseModule):

    def get_report(self, request, response):
        if response.status_code // 100 == 5:
            return "server error"
