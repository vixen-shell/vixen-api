import json

def read_json(path: str) -> dict:
    with open(path, 'r', encoding = 'utf-8') as file:
        return json.load(file)
    
def write_json(path: str, data: dict):
    with open(path, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)

class SettingFile:
    def __init__(self, path: str):
        self.path = path
        self.data = read_json(path)
    
    def save(self):
        write_json(self.path, self.data)