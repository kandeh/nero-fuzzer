import string

import lxml.html

from .base_module import BaseModule


class HTMLParamExtractor(BaseModule):

    PARAM_CHARS = f"{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}_-"

    def process_response(self, request, response):
        if len(response.text) < 1:
            return

        doc = lxml.html.fromstring(response.text.encode())

        for inp in doc.xpath("//input"):
            if inp.name and len(inp.name) > 0:

                f = True
                for ch in inp.name:
                    if not ch in self.PARAM_CHARS:
                        f = False
                        continue
                if f:
                    self.dynamic_memory.add_one("param", inp.name)
