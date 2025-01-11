import os
import sys
import json
import numpy as np
from tfm_BERTTokensBuilder import BERTTokensBuilder
from tfm_LabelLoader import LabelLoader
import pandas as pd

class EURLEX57KDataFrameBuilder:
    def __init__(self, baseDir, fileIndex, dataFrameFileName):
        self.fileIndex = fileIndex
        self.baseDir = baseDir
        self.dataFrameFileName = dataFrameFileName
        self.listFiles = {}
        self.dataSet = []
        self.bertTknzr = BERTTokensBuilder()
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

    def toDict(self, fileName, jsonObj):
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
        item['input_ids'], item['attention_mask'] =  self.dataToTokens(filteredData)
        item['labels'] = self.getLabels(labels)

        return item
    
    def getLabels(self, labels):
        labelsArray = np.zeros(self.numLabels)
        for label in labels:
            idx = self.labelsDict.get(f"'{label}'")
            labelsArray[idx] = 1.0

        return labelsArray
      
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

    def dataToTokens(self, data):
        self.bertTknzr.reset()
        lines = self.getLines(data)
        inputIds, attentionMask = self.bertTknzr.tokenize(lines)
        
        return inputIds, attentionMask

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
        print('Building data frame')
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
        item =  self.toDict(fileName, jsonObj)
        return item

    def saveDataFrame(self):
        print('Init CSV saving')
        fullFileName = f'{self.baseDir}/{self.dataFrameFileName}'
        df = pd.DataFrame(self.dataSet)
        np.set_printoptions(threshold=sys.maxsize)
        df.to_csv(fullFileName)
        print('CSV DataFrame Created')

        
if __name__ == '__main__':
    os.system("clear")
    print('Build CSV Dataframe\n')
    baseDir = '.'
    EURLEX57KDataFrameBuilder(baseDir, 'FilesIndex.txt', 'EURLEX57KDataFrame.csv')
        
