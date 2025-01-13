import json

class LabelLoader:
    def __init__(self, baseDir):
        fp = open(f'{baseDir}/EURLEX57K.json')
        self.labels = json.load(fp)
        fp.close()
