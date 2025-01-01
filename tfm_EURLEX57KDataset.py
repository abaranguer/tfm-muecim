import torch
import json
import numpy as np
from tfm_BERTTokenizer import BERTTokenizer


class EURLEX57KDataset(torch.utils.data.Dataset):
    def __init__(self, fileIndex):
        self.fileIndex = fileIndex
        self.listFiles = {}
        self.bertTknzr = BERTTokenizer()
        self.loadFiles()
        
    def __getitem__(self, idx):
        fileName = self.listFiles[idx]
        fd = open(fileName, 'r')
        jsonObj = json.load(fd)
        fd.close()
        item =  self.toTensor(jsonObj)
        return item
    
    def __len__(self):
        return len(self.listFiles)

    def loadFiles(self):
        fd = open(self.fileIndex, "r")
        lines = fd.readlines()
        for line in lines:
            tokens = line.split(',')
            key = tokens[0]
            value = tokens[1].strip()
            self.listFiles[int(key)] = value

        fd.close()

    def toTensor(self, jsonObj):
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
        item['data'] =  self.dataToTensor(filteredData)
        item['labels'] = self.getLabels(labels)

        return item
    
    def getLabels(self, labels):
        labelsInt = [int(label) for label in labels]
 
        return torch.tensor(labelsInt)

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
        tokensTensor = self.bertTknzr.tokenize(lines)
        
        return tokensTensor

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
        # res, per ara.
        
        return dataRaw

if __name__ == '__main__':
    ds = EURLEX57KDataset('FilesIndexShort.txt')
    for i in range(5):
        item = ds.__getitem__(i)
        print(i, 'item["data"]: ', item["data"].shape)
        print(i, 'item["labels"]: ', item["labels"])
        print('data: ', item['data'][0:10])
