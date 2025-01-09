import os
import torch
import json
import numpy as np
from tfm_BERTTokensTensorBuilder import BERTTokensTensorBuilder
from tfm_LabelLoader import LabelLoader
import pandas as pd

class EURLEX57KTensorDatasetBuilder:
    def __init__(self, baseDir, fileIndex, tensorDatasetFileName):
        self.fileIndex = fileIndex
        self.baseDir = baseDir
        self.tensorDatasetFileName = tensorDatasetFileName
        self.listFiles = {}
        self.dataSet = []
        self.bertTknzr = BERTTokensTensorBuilder()
        labelLoader = LabelLoader(self.baseDir)
        self.numLabels = len(labelLoader.labels)
        self.labelsDict = {}
        self.loadLabelsDict()
        self.loadFiles()
        self.buildDataFrame()
        self.saveDataFrame()
        
    def loadFiles(self):
        fd = open(f'{self.baseDir}/{self.fileIndex}', 'r')
        lines = fd.readlines()
        for line in lines:
            tokens = line.split(',')
            key = tokens[0]
            value = tokens[1].strip()
            self.listFiles[int(key)] = value

    def loadLabelsDict(self):
        fd = open(f'{self.baseDir}/LabelIndex.txt', 'r')
        lines = fd.readlines()
        fd.close()

        for line in lines:
            toks = line.split(',')
            index = toks[0]
            label = toks[1].strip()
            self.labelsDict[label] = int(index)

    def toTensor(self, fileName, jsonObj):
        labels = jsonObj.get('concepts')
        title = jsonObj.get('title')
        header = jsonObj.get('header')
        recitals = jsonObj.get('recitals')
        mainBody = jsonObj.get('main_body')
        attachments = jsonObj.get('attachments')
        
        rawFullText = [title, header, recitals, mainBody, attachments]
                
        rawFlattenedData = self.getData(rawFullText)
        filteredData =  self.filterData(rawFlattenedData)
        item = {}
        item['fileName'] = fileName
        item['input_ids'], item['attention_mask'] =  self.dataToTensor(filteredData)
        item['labels'] = self.getLabels(labels)

        return item
    
    def getLabels(self, labels):
        labelsArray = np.zeros(self.numLabels)
        for label in labels:
            idx = self.labelsDict.get(f"'{label}'")
            labelsArray[idx] = 1.00
 
        return torch.tensor(labelsArray)

    def getData(self, raw):
        data = []
        for item in raw:
            itemShape = len(np.shape(item))
            if (itemShape == 1):
                for part in raw:
                    data.append(part)
            else:
                data.append(item)

        return data

    def dataToTensor(self, data):
        self.bertTknzr.reset()
        lines = self.getLines(data)
        tokensTensor, attentionMask = self.bertTknzr.tokenize(lines)
        
        return tokensTensor, attentionMask

    def getLines(self, data):
        linesFlattened = []
        for item in data:
            if type(item) == str:
                lines  = item.split('\n')
            else:
                lines = item[0].split('\n')

            for line in lines:
                linesFlattened.append(line)
            
        return linesFlattened;
        
    def filterData(self, dataRaw):
        # at the moment, do nothing.         
        return dataRaw

    def buildDataFrame(self):
        numFiles = len(self.listFiles)
        for ix in range(numFiles):
            item = self.getElementFromFile(ix)
            self.dataSet.append(item)
            if (ix % 1000 == 0):
                print(f'Index: {ix}')

    def getElementFromFile(self, idx):
        fileName = self.listFiles[idx]
        fd = open(f'{self.baseDir}/{fileName}', 'r')
        jsonObj = json.load(fd)
        fd.close()
        item =  self.toTensor(fileName, jsonObj)
        return item

    def saveDataFrame(self):
        fullFileName = f'{self.baseDir}/{self.tensorDatasetFileName}'
        torch.save(self.dataSet, fullFileName)

    
if __name__ == '__main__':
    os.system("clear")
    print('Build tensor dataset\n')
    baseDir = '.'
    EURLEX57KTensorDatasetBuilder(baseDir,'FilesIndex.txt', 'EURLEX57KTensorDataset.pt')
        
