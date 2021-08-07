import re
import string

from nero.modules import BaseDataExtractor
from nero.utils import get_all_data


class RawBodyExtractor(BaseDataExtractor):

    # TODO: compile all regexes
    def process_response(self, request, response):
        data = set()
        text = response.text

        # remove html ending tags because they have '/' while they are not path
        text = re.sub(r"</[\s]*[a-zA-Z]+[\s]*>", "<>", text)

        text = text.replace("/*", " ")
        text = text.replace("*/", " ")

        # email
        data.update(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text))
        
        # path
        data.update(re.findall(r"(/[^\]\[\(\)\\\n><:\'\"!#$^&*`~+,|=;]+)+", text))

        # uuid
        # https://stackoverflow.com/questions/136505/searching-for-uuids-in-text-with-regex
        data.update(re.findall(r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}", text))

        self.save_data(request, response, data)
