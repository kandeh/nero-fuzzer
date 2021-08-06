
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

# TODO: application/yaml
ALL_CONTENT_TYPES = [
    "application/json",
    "multipart/form-data",
    "application/x-www-form-urlencoded",
]

class Request:
    def __init__(self):
        self.method = "GET"
        self.path = "/"
        self.params = {}
        self.headers = {}
        self.cookies = {}
        self.data = {}
        self.content_type = None
