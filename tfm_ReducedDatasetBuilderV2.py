import os
import json
import pickle
from tfm_DatasetAnalyzer import DatasetAnalyzer

class ReducedDataset50LabelsBuilder:
    def __init__(self, baseDir, fileIndex):
        self.fileIndex = fileIndex
        self.baseDir = baseDir
        self.minLabelSet = []
        self.reducedFileList = {}
        self.minLabelSetIx2Label = {}
        self.minLabelSetLabel2Ix = {}
        self.jsonFiles = [0 for i in range(57000)]
        self.da = DatasetAnalyzer(baseDir, fileIndex)
        
        self.reduceLabels()
        self.reduceFileList()

    def reduceLabels(self):
        #self.da.buildFilesPerLabelFile()
        self.da.loadFilesPerLabelFile()
        self.filesPerLabel = self.da.filesPerLabel
        print('len(filesPerLabel): ', len(self.filesPerLabel))

        print('check 1: ', sum(self.jsonFiles))
        ixLabel = 0
        for key in self.filesPerLabel.keys():
            self.minLabelSet.append(key)
            self.minLabelSetIx2Label[ixLabel] = key
            self.minLabelSetLabel2Ix[key] = ixLabel
            ixLabel = ixLabel + 1
            files = self.filesPerLabel.get(key)
            for file in files:
                self.jsonFiles[int(file)] = 1

            numFiles = sum(self.jsonFiles)
            pc = numFiles * 100.0 / 57000.0

            if ixLabel == 50:
                print('50 labels achieved')
                print('Files in the reduced dataset: ', sum(self.jsonFiles))
                break

        print('minLabelSet length: ', len(self.minLabelSetIx2Label))
        self.saveMinLabelSet()

    def reduceFileList(self):
        fd = open(self.fileIndex, 'r')
        lines = fd.readlines()
        fd.close()

        ixFull = 0
        ixReduced = 0
        for line in lines:
            [_, jsonFile] = line.split(',')
            jsonFile = jsonFile.strip()
            if self.jsonFiles[ixFull] == 1:
                self.reducedFileList[ixReduced] = jsonFile
                ixReduced = ixReduced + 1
            ixFull = ixFull + 1

        print(f'Reduced file list length : {len(self.reducedFileList)}') 
        self.saveReducedFileList()
        
    def saveMinLabelSet(self):
        with open(f'{self.baseDir}/50LabelsLabelSet.dat', 'wb') as fd:
            pickle.dump(self.minLabelSet, fd)
        with open(f'{self.baseDir}/50LabelsLabelSetIx2Label.dat', 'wb') as fd:
            pickle.dump(self.minLabelSetIx2Label, fd)
        with open(f'{self.baseDir}/50LabelsLabelSetLabel2Ix.dat', 'wb') as fd:
            pickle.dump(self.minLabelSetLabel2Ix, fd)

    def saveReducedFileList(self):
        fd = open(f'{self.baseDir}/50LabelsLabelSetFileIndex.txt', 'w')
        for item in self.reducedFileList.items():
            fd.write(f'{item[0]},{item[1]}\n')
        fd.close()
            

if __name__ == '__main__':
    print('Init')
    rdb = ReducedDataset50LabelsBuilder('.','FilesIndex.txt')
    print('Done!')
        
    
