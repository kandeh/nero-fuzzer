import os
import random
import re
import string
from uuid import UUID
from urllib.parse import urlparse


def load_data_from_file(file_path):
    ret = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            ret.append(line)
    return ret

def load_data(data_name):
    return load_data_from_file(f"./data/{data_name}.txt")


def uniform(arr):
    if len(arr) < 1:
        return None
    if isinstance(arr, set):
        arr = tuple(arr)
    return arr[random.randint(0, len(arr) - 1)]


def get_path(url):
    url = url.lstrip("/.")
    url = urlparse(url).path

    if len(url) < 1:
        return "/"

    if not url[0] == "/":
        url = "/" + url

    return url


def random_string(length):
   letters = string.printable
   return ''.join(random.choice(letters) for i in range(length))


# https://www.geeksforgeeks.org/longest-repeating-and-non-overlapping-substring/
def longest_repeated_substring(str):
    n = len(str)
    LCSRe = [[0 for x in range(n + 1)]
                for y in range(n + 1)]
 
    res = "" # To store result
    res_length = 0 # To store length of result
 
    # building table in bottom-up manner
    index = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
             
            # (j-i) > LCSRe[i-1][j-1] to remove
            # overlapping
            if (str[i - 1] == str[j - 1] and
                LCSRe[i - 1][j - 1] < (j - i)):
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1
 
                # updating maximum length of the
                # substring and updating the finishing
                # index of the suffix
                if (LCSRe[i][j] > res_length):
                    res_length = LCSRe[i][j]
                    index = max(i, index)
                 
            else:
                LCSRe[i][j] = 0
 
    # If we have non-empty result, then insert
    # all characters from first character to
    # last character of string
    if (res_length > 0):
        for i in range(index - res_length + 1,
                                    index + 1):
            res = res + str[i - 1]
 
    return res


def get_all_data(data):
    ret = set()

    if isinstance(data, str) or isinstance(data, int) or isinstance(data, float):
        return set([data])

    if isinstance(data, dict):
        for key in data.keys():
            ret.add(key)
            ret.update(get_all_data(data[key]))

    if isinstance(data, list):
        for element in data:
            ret.update(get_all_data(element))

    return ret


WEB_PATH_EXTS = [
    ".cgi",
    ".txt",
    ".rss",
    ".html",
    ".htm",
    ".xhtm",
    ".xml",
    ".js",
    ".css",
    ".php",
    ".php3",
    ".asp",
    ".aspx",
    ".jsp",
    ".jspx",
    ".json",
    ".yaml",
    ".yml",
]
MAX_PATH_LENGTH = 2048

def can_be_path(text):
    if len(text) <= 1 or len(text) > MAX_PATH_LENGTH:
        return False

    if text.count("/") > 1:
        return True

    if text[0] == "/":
        return True
    
    for ext in WEB_PATH_EXTS:
        if text.endswith(ext):
            return True
    
    return False


def can_be_email(text):
    return bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))

def can_be_uuid(text):
    try:
        UUID(text).version
        return True
    except ValueError:
        return False


def predict_text_data_type(data):
    data = str(data)


def get_path_candidates(arr):
    ret = set()
    for element in arr:
        element = str(element)
        if can_be_path(element):
            ret.add(element)
    return ret


def get_uuid_candidates(arr):
    ret = set()
    for element in arr:
        element = str(element)
        if can_be_uuid(element):
            ret.add(element)
    return ret


def get_email_candidates(arr):
    ret = set()
    for element in arr:
        element = str(element)
        if can_be_email(element):
            ret.add(element)
    return ret



def empty_object():
    return type('', (), {})()


# print(get_all_data({
#     "data": {
#         "v": 3.14,
#         "x": 2,
#         "arr": ["77", 33, 99, "alireza"]
#     }
# }))

# print(can_be_email("test@test.test"))