import json

class Config:
    datatableKey: str
    fumenKey: str

    def __init__(self) -> None:
        with open('config.json') as f:
            d = json.load(f)
            self.datatableKey = d['datatableKey']
            self.fumenKey = d['fumenKey']

config: Config = Config()



