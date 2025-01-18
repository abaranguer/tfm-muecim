import os
import json
import pickle
from tfm_DatasetAnalyzer import DatasetAnalyzer

class ReducedDatasetBuilder:
    def __init__(self, baseDir, fileIndex):
        self.fileIndex = fileIndex
        self.baseDir = baseDir
        self.reducedLabelsList = {}
        self.reducedFilesList = {}
        self.minLabelSet = []
        self.da = DatasetAnalyzer(baseDir, fileIndex)
        self.filesPerLabel = self.da.loadFilesPerLabelFile()         
        self.jsonFiles = [0 for i in range(57000)]
        
        print('check 1: ', sum(jsonFiles))
        for key in self.filesPerLabel.keys():
            self.minLabelSet.append(key)
            files = self.filesPerLabel.get(key)
            for file in files:
                self.jsonFiles[int(file)] = 1

            numFiles = sum(self.jsonFiles)
            pc = numFiles * 100.0 / 57000.0

            if pc >= 95.0:
                print('Percentage achieved')
                print('Files in the reduced dataset: ', sum(self.jsonFiles))
                break

        print('minLabelSet: ', len(self.minLabelSet))
        self.saveMinLabelSet()
        
    def saveMinLabelSet(self):
        with open('ReducedLabelList.dat', 'wb') as fd:
            pickle.save(self.minLabelSet)

if __name__ == '__main__':
    print('Init')
    ReducedDatasetBuilder('.', 'FilesIndex.txt')
    print('Done!')
        
    
