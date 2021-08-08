import threading
import json

from flask import Flask


class UI:

    def __init__(self, static_memory, dynamic_memory, reports):
        self.static_memory = static_memory
        self.dynamic_memory = dynamic_memory
        self.reports = reports

        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index_view)
        self.app.add_url_rule('/dynamic_memory', 'dynamic_memory', self.dynamic_memory_view)
        self.app.add_url_rule('/reports', 'reports', self.reports_view)

        thread = threading.Thread(target=self.app.run)
        thread.start()


    def index_view(self):
        return """
            <h1>Nero Fuzzer</h1>
            <a href="/reports">reports</a>
            <br>
            <a href="/dynamic_memory">dynamic memory</a>
        """


    def dynamic_memory_view(self):
            content = json.dumps(self.dynamic_memory.data, default=tuple, sort_keys=True, indent=4)
            content = f"<pre>{content}</pre>"
            return content


    def reports_view(self):
            content = json.dumps(self.reports, default=tuple, sort_keys=True, indent=4)
            content = f"<pre>{content}</pre>"
            return content
