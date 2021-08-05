
class BaseModule:

    def __init__(self, static_memory, dynamic_memory):
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory


    def generate_request(self):
        pass
        

    def process_response(self, request, response):
        pass


    def get_report(self, request, response):
        pass
