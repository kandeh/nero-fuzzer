from .utils import uniform


class Memory:

    MAX_COOKIE_VALUES = 100

    def __init__(self):
        self.data = {}
        self.cookies = {}


    def add_one(self, label, data):
        current_data = self.data.get(label, set())
        current_data.add(data)
        self.data[label] = current_data


    def add_many(self, label, data):
        current_data = self.data.get(label, set())
        current_data.update(data)
        self.data[label] = current_data


    def get_one_random(self, label):
        all_values = self.data.get(label, set())
        return uniform(all_values)


    def add_cookie(self, name, value):
        values = self.cookies.get(name, [])
        values.append(value)

        if len(values) > self.MAX_COOKIE_VALUES:
            values = values[-self.MAX_COOKIE_VALUES:]
        
        self.cookies[name] = values


    def get_random_full_cookies(self):
        ret = {}

        for name in self.cookies.keys():
            ret[name] = uniform(self.cookies[name])

        return ret

