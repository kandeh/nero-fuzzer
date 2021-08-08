import re

from .base_module import BaseModule
from nero.request import Request, ALL_CONTENT_TYPES
from nero.utils import (
    uniform,
    get_path,
    longest_repeated_substring,
)


class DynamicPathDiscovery(BaseModule):

    IGNORE_SUFFIX = [
        ".css",
        ".png",
        ".gif",
        ".jpg",
        ".jpeg",
        ".ttf",
        ".pdf",
        ".ico",
        ".svg",
        ".woff",
        ".woff2",
        ".eot",
        ".zip",
        ".rar",
        ".rar",
        ".tar.gz",
    ]

    def __init__(self, static_memory, dynamic_memory):
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.tried = set()


    def generate_request(self):
        all_paths = self.dynamic_memory.data.get("path", [])
        ignore = set(self.tried)

        for path in all_paths:
            for suf in self.IGNORE_SUFFIX:
                if path.endswith(suf) or path.endswith(suf + "/"):
                    ignore.add(path)

        random_path = uniform(all_paths, ignore)
        if random_path == None:
            return None

        request = Request()
        request.method = uniform(["GET", "POST", "PUT", "DELETE", "PATCH"])
        request.path = random_path
        request.content_type = uniform(ALL_CONTENT_TYPES)
        request.cookies = self.dynamic_memory.get_random_full_cookies()

        if random_path.endswith(".js") and request.method == "GET":
            self.tried.add(random_path)

        return request
