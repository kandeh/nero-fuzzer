import re
import yaml

from .base_module import BaseModule
from nero.request import Request
from nero.utils import (
    get_path,
    get_path_candidates,
    get_uuid_candidates,
    get_email_candidates,
)


class BaseDataExtractor(BaseModule):

    def save_data(self, request, response, data):
        for element in get_path_candidates(data):
            self.dynamic_memory.add_one("path", get_path(element))

        for element in get_uuid_candidates(data):
            self.dynamic_memory.add_one("uuid", element)

        for element in get_email_candidates(data):
            self.dynamic_memory.add_one("email", element)
