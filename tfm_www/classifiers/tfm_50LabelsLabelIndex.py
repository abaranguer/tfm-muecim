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
        with open(f'{self.baseDir}/50LabelsLabelSetIx2Label.dat','rb') as fd:
            self.id2label = pickle.load(fd)
        with open(f'{self.baseDir}/50LabelsLabelSetLabel2Ix.dat','rb') as fd:
            self.label2id = pickle.load(fd)
            
        self.numLabels = len(self.id2label)
