import json
class User:
    def __init__(self, name):
        self.name = name

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def __str__(self):
        return self.name + " "

