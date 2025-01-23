import json
import pickle

class LabelIndex:
    def __init__(self,baseDir):
        self.baseDir = baseDir
        self.id2label = {}
        self.label2id = {}
        self.numLabels = 0
        
        self.readDictionaries()

    def readDictionaries(self):
        with open(f'{self.baseDir}/ReducedLabelSetIx2Label.dat','rb') as fd:
            self.id2label = pickle.load(fd)
        with open(f'{self.baseDir}/ReducedLabelSetLabel2Ix.dat','rb') as fd:
            self.label2id = pickle.load(fd)
            
        self.numLabels = len(self.id2label)


if __name__ == '__main__':
    print('Init')
    labelIndex = LabelIndex('/content/drive/MyDrive/TFM-MUECIM')
    print(f'ix = 35; label = {labelIndex.id2label.get(35)}')
    print(f'ix = 200; label = {labelIndex.id2label.get(200)}')    
    print(f'label = "3173": ix = {labelIndex.label2id.get("3173")}')    
    print(f'label = "2081": ix = {labelIndex.label2id.get("2081")}')    
    print('Done!')
