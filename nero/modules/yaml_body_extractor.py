import re
import yaml

from nero.request import Request
from nero.modules import BaseDataExtractor
from nero.utils import get_all_data


class YAMLBodyExtractor(BaseDataExtractor):

    def process_response(self, request, response):
        data = None

        try:
            data = yaml.safe_load(response.text)
        except Exception as excp:
            return None

        if data == None or isinstance(data, str):
            return None

        data = get_all_data(data)
        self.save_data(request, response, data)
