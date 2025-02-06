import os
import json
import pickle
from tfm_DatasetAnalyzer import DatasetAnalyzer

class ReducedDataset50LabelsBuilder:
    def __init__(self, baseDir, fileIndex, fileFreqs):
        self.fileIndex = fileIndex
        self.fileFreqs = fileFreqs
        self.baseDir = baseDir
        self.index2Label = {}
        self.label2Index = {}
        self.lfSortedKeys = []
        self.lfOrdered = []
        
        self.reduceLabels()

    def loadLabelFreqs(self):
        with open(self.fileFreqs,'rb') as fd:
            lf = pickle.load(fd)

        lfKeys = lf.keys()

        self.lfSortedKeys = sorted(lf, key = lf.get, reverse = True)

        for lfKey in self.lfSortedKeys:
            self.lfOrdered.append(lf.get(lfKey))
            
    def reduceLabels(self):
        self.loadLabelFreqs()

        with open('FilesPerLabel.dat', 'rb') as fpld:
           fpl = pickle.load(fpld)

        fileIndexes = []
        for labelKey in self.lfSortedKeys[50:100]:
            filesPerLabel = fpl.get(labelKey)
            for filePerLabel in filesPerLabel:
                if filePerLabel not in fileIndexes:
                    fileIndexes.append(filePerLabel)

        with open('FilesIndex.txt','r') as fiFd:
            fiBase = fiFd.readlines()

        k = 0
        with open(
                '50LabelsLabelSetFileIndex.txt',
                'w'
        ) as fd50labelsFileIndex:
            for fileIndex in fileIndexes:
                line = fiBase[fileIndex]
                tokens = line.split(',');
                fd50labelsFileIndex.write(f'{k},{tokens[1]}')
                k += 1

        self.saveMinLabelSet()

    def saveMinLabelSet(self):
        k = 0
        for labelKey in self.lfSortedKeys[50:100]:
            self.index2Label[k] = labelKey
            self.label2Index[labelKey] = k
            k += 1

        with open(f'{self.baseDir}/50LabelsLabelSet.dat', 'wb') as fd:
            pickle.dump(self.lfSortedKeys[50:100], fd)
        with open(f'{self.baseDir}/50LabelsLabelSetIx2Label.dat', 'wb') as fd:
            pickle.dump(self.index2Label, fd)
        with open(f'{self.baseDir}/50LabelsLabelSetLabel2Ix.dat', 'wb') as fd:
            pickle.dump(self.label2Index, fd)
            

if __name__ == '__main__':
    print('Init')
    rdb = ReducedDataset50LabelsBuilder(
        '.',
        'FilesIndex.txt',
        'LabelsFreqs.dat')
    print('Done!')
        
    
