import random
import uuid

import editdistance

from .utils import uniform, random_string


class DataProducer:

    SIMILAR_LABELS = [
        ["username", "user", "name", "id", "email", "log"],
        ["password", "pass", "secret", "token", "credential", "cred", "pwd"],
        ["uuid", "id"],
    ]

    def __init__(self):
        # self.data_sources = ["random"]
        self.data_sources = []

    
    def add_source(self, data_source):
        if data_source != None:
            self.data_sources.append(data_source)


    def get_similar_labels(self, label):
        label = label.lower()
        ret = set()
        ret.add(label)

        for group in self.SIMILAR_LABELS:
            for other_label in group:

                if other_label in label:
                    ret.update(group)
                    break

                distance = editdistance.eval(other_label, label)
                if distance <= 2:
                    ret.update(group)
                    break

        return ret


    def get(self, label):
        ret = None
        random.shuffle(self.data_sources)
        labels = list(self.get_similar_labels(label))
        random.shuffle(labels)
        for source in self.data_sources:
            if source == "random":
                return random_string(32)
            for l in labels:
                ret = source.get_one_random(l)
                if ret != None:
                    return ret

        if ret == None:
            return uuid.uuid4().hex


# dp = DataProducer()
# print(dp.get_similar_labels("user_id"))
