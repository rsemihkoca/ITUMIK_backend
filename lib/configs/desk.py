import json
from lib.utils.configs import Configs

class DeskManager:
    """
    TODO: Floor1.Desk1.Chair1 gibi bir yapı oluşturmayı dene
    """

    def __init__(self, file_path):
        self.data = DeskManager.read_json(file_path)

    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data


    def get_status(self):
        return self.data

    def get_subscribes(self):
        subscribes = []
        for floor, desks in self.data.items():
            for desk in desks:
                subscribe = f"{floor}/{desk}"
                subscribes.append(subscribe)
        return subscribes