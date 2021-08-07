import string
import json
import yaml

from .base_module import BaseModule


class JsonAndYamlParamExtractor(BaseModule):

    def process_response(self, request, response):
        text = None

        try:
            json.loads(response.text)
            text = response.text
        except:
            try:
                data = yaml.safe_load(response.text)
                if data and not isinstance(data, str):
                    text = response.text
            except:
                pass

        if text == None:
            return

        params = set()

        param_chars = f"{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}_-"
        
        param = ""
        for ch in text:
            if ch in param_chars:
                param = param + ch
            else:
                if len(param) < 24 and len(param) > 0:
                    params.add(param)
                param = ""

        for p in params:
            self.dynamic_memory.add_one("param", p)
