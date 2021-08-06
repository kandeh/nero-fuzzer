
# TODO: TRACE and CONNECT method?
All_METHODS = [
    "GET",
    "POST",
    "DELETE",
    "PUT",
    "PATCH",
    "HEAD",
    "OPTIONS",
]


class Request:
    def __init__(self):
        self.method = "GET"
        self.path = "/"
        self.params = {}
        self.headers = {}
        self.cookies = {}
        self.data = {}
