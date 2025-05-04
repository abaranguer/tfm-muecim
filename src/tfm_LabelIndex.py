import numpy as np
import json

class LabelIndex:
    def __init__(self,baseDir):
        self.baseDir = baseDir
        self.id2label = {}
        self.label2id = {}

        self.readlines()
        self.buildDictionaries()

    def readlines(self):
        fd = open(f'{self.baseDir}/LabelIndex.txt','r')
        self.lines = fd.readlines()
        fd.close()

    def buildDictionaries(self):
        for line in self.lines:
            tokens = line.split(',')
            key = tokens[0]
            value = tokens[1].strip()
            singleQuotesRemovedValue = value[1:-1]
            self.id2label[int(key)] = singleQuotesRemovedValue
            self.label2id[singleQuotesRemovedValue] = int(key)

if __name__ == '__main__':
    print('Init')
    labelIndex = LabelIndex('/content/drive/MyDrive/TFM-MUECIM')
    print(f'ix = 35; label = {labelIndex.id2label.get(35)}')
    print(f'ix = 1085; label = {labelIndex.id2label.get(1085)}')    
    print(f'label = "851": ix = {labelIndex.label2id.get("851")}')    
    print(f'label = "1000": ix = {labelIndex.label2id.get("1000")}')    
    print('Done!')
