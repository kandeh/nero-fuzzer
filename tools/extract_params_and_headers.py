import glob
import json
import string
from pathlib import Path

AUTH_HEADER_WORDS = [
    "auth",
    "key",
    "api",
    "secret",
    "token",
    "cred",
    "access",
    "session",
    "jwt",
    "hash",
    "client",
    "password",
    "pwd",
]

CSRF_HEADER_WORDS = [
    "csrf",
    "xsrf",
]


params = set()
auth_headers = set()
csrf_headers = set()


def extract(data):
    global params
    global auth_headers

    if isinstance(data, dict) and \
        "name" in data and \
        "type" in data and \
        "in" in data and \
        isinstance(data['name'], str):

        for ch in data['name'].lower():
            if not ch in f"{string.ascii_lowercase}{string.digits}-_":
                return

        if "__" in data['name']:
            return

        if data['in'] == "header":
            for sub in AUTH_HEADER_WORDS:
                if sub in data['name'].lower():
                    auth_headers.add(data['name'])
                    break

            for sub in CSRF_HEADER_WORDS:
                if sub in data['name'].lower():
                    csrf_headers.add(data['name'])
                    break
            return

        params.add(data['name'])

    if isinstance(data, dict):
        for sub in data.values():
            extract(sub)

    if isinstance(data, list):
        for sub in data:
            extract(sub)


all_files = glob.glob(f"{Path.home()}/data/swagger-files/*")
for file_path in all_files:
    with open(file_path, "r") as file:
        text = file.read()
        try:
            data = json.loads(text)
        except:
            continue
        extract(data)

with open("../data/params.txt", "w") as file:
    for param in params:
        print(param, file=file)

with open("../data/auth_headers.txt", "w") as file:
    for header in auth_headers:
        print(header, file=file)

with open("../data/csrf_headers.txt", "w") as file:
    for header in csrf_headers:
        print(header, file=file)
