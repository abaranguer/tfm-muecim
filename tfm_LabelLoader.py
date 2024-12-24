import json

class LabelLoader:
    def __init__(self):
        fp = open('data/datasets/EURLEX57K/EURLEX57K.json')
        self.labels = json.load(fp)
        print(f'Total d\'etiquetes: {len(self.labels)}')
        fp.close()
