import os
import logging
import threading
from urllib.parse import urlparse

from .utils import load_data_from_file, load_data, empty_object
from .memory import Memory
from .modules import BaseDataExtractor
from .ui import UI
from .fuzzer import NeroFuzzer

reports = []
static_memory = Memory()
dynamic_memory = Memory()

static_memory.add_many("param", load_data("params"))
static_memory.add_many("email", load_data("emails"))
static_memory.add_many("username", load_data("usernames"))
static_memory.add_many("password", load_data("passwords"))
static_memory.add_many("path", load_data("paths"))


def get_target():
    nero_target = os.environ.get("NERO_TARGET", None)

    if nero_target == None:
        logging.fatal("NERO_TARGET env must be set.")
        exit(1)
    
    target_url = urlparse(nero_target)
    if not target_url.scheme in ["http", "https"]:
        logging.fatal(f"scheme {target_url.scheme} is not valid.")
        exit(1)
    
    return f"{target_url.scheme}://{target_url.netloc}"

def run_fuzzer():
    NeroFuzzer(nero_target, static_memory, dynamic_memory, reports)

if __name__ == "__main__":
    nero_target = get_target()
    nero_dict_path = os.environ.get("NERO_DICT_PATH", None)

    # TODO:
    # nero_source_path = os.environ.get("NERO_SOURCE_PATH", None)

    if nero_dict_path != None:
        data = load_data_from_file(nero_dict_path)
        data_extractor = BaseDataExtractor(static_memory, dynamic_memory)
        data_extractor.save_data(None, None, data)

        for element in data:
            dynamic_memory.add_one("credential", element)
            dynamic_memory.add_one("username", element)

    # start web ui
    UI(static_memory, dynamic_memory, reports)

    for i in range(1):
        threading.Thread(target=run_fuzzer).start()
