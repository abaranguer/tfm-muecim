import os
import json
import pickle

class ReducedDatasetAnalyzer:
    def __init__(self, baseDir, fileIndex):
        self.fileIndex = fileIndex
        self.baseDir = baseDir
        self.labels = {}
        self.filesPerLabel = {}
    
    def countLabels(self):
        fd = open(self.fileIndex, 'r')
        lines = fd.readlines()
        fd.close()
        i = 0
        for line in lines:
            [_, jsonFile] = line.split(',')
            djf = open(jsonFile.strip(), 'r')
            jsonFile = json.load(djf)
            djf.close()
            i = i + 1
            if (i % 1000 == 0):
                print(f'i: {i}')
            labels = jsonFile.get('concepts')
            for label in labels:
                value = self.labels.get(label)
                if (value == None):
                    self.labels[label] = 1
                else:
                    self.labels[label] = self.labels[label] + 1

    def buildFilesPerLabel(self):
        fd = open(self.fileIndex, 'r')
        lines = fd.readlines()
        fd.close()
        i = 0
        for line in lines:
            [fileIndex, jsonFile] = line.split(',')
            djf = open(jsonFile.strip(), 'r')
            jsonFile = json.load(djf)
            djf.close()
            i = i + 1
            if (i % 1000 == 0):
                print(f'i: {i}')
            labels = jsonFile.get('concepts')
            for label in labels:
                value = self.filesPerLabel.get(label)
                if (value == None):
                    files = [int(fileIndex)]
                    self.filesPerLabel[label] = files
                else:
                    files = self.filesPerLabel[label]
                    files.append(int(fileIndex))
                    self.filesPerLabel[label] = files
            
    def sortLabelsByFreq(self):
        self.labels = dict(sorted(self.labels.items(), key = lambda item: item[1])) 

    def buildLabelsFreqsFile(self):
        self.countLabels()
        
        with open(f'{self.baseDir}/ReducedLabelsFreqs.dat', 'wb') as fd:
            pickle.dump(self.labels, fd)
            
        print('Done!')

    def buildFilesPerLabelFile(self):
        self.buildFilesPerLabel()
        
        with open(f'{self.baseDir}/ReducedFilesPerLabel.dat', 'wb') as fd:
            pickle.dump(self.filesPerLabel, fd)

        print('Done!')
       
    def loadLabelsFreqsFile(self): 
        with open(f'{self.baseDir}/ReducedLabelsFreqs.dat', 'rb') as fd:
            self.labels = pickle.load(fd)

        print('File read.')

    def loadFilesPerLabelFile(self): 
        with open(f'{self.baseDir}/ReducedFilesPerLabel.dat', 'rb') as fd:
            self.filesPerLabel = pickle.load(fd)

        print('File read.')
        
    def showLabelsCountSorted(self):
        self.sortLabelsByFreq()
        accum = 0
        for label in self.labels.keys():
            freq =  self.labels.get(label)
            accum = accum + freq
            print(f'Label: {label}; freq: {freq}; accum: {accum}')

    def showSorted(self):
        self.sortLabelsByFreq()
        accum = 0
        for label in self.labels.keys():
            freq =  self.labels.get(label)
            accum = accum + freq
            print(f'Label: {label}; freq: {freq}; accum: {accum}')

            
if __name__ == '__main__':
    os.system("clear")
    print('Build labels list (Reduced EURLEX57K)\n')
    baseDir = '.'
    
    da = ReducedDatasetAnalyzer(baseDir, 'ReducedFileIndex.txt')
    da.buildLabelsFreqsFile()
    print(f'Total labels found: {len(da.labels)}')
    da.showSorted()
