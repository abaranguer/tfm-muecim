import os
import torch
import pandas as pd

class EURLEX57KDataset(torch.utils.data.Dataset):
    def __init__(self, baseDir, DataFrameFile):
        self.DataFrameFile = DataFrameFile
        self.baseDir = baseDir
        self.fullPath = f'{baseDir}/{DataFrameFile}'
        self.dataFrame = pd.read_csv(self.fullPath)
        self.item = {}
        
    def __getitem__(self, idx):
        itemDf = self.dataFrame.iloc[idx]
        self.item = {}
        self.item['fileName'] = itemDf['fileName']
        self.setItemInputIds(itemDf)
        self.setItemAttentionMask(itemDf)
        self.setItemLabels(itemDf) 
        return self.item
    
    def __len__(self):
        dfLength =  len(self.dataFrame)
        return dfLength

    def setItemInputIds(self, itemDf):
        fieldName = 'input_ids'
        self.setItemIntArray(itemDf, fieldName)
        
    def setItemAttentionMask(self, itemDf):
        fieldName = 'attention_mask'
        self.setItemIntArray(itemDf, fieldName)

    def setItemIntArray(self, itemDf, fieldName):
        intArrayStr = itemDf[fieldName]
        toks = [int(tok.strip()) for tok in intArrayStr[1:-1].split()]
        self.item[fieldName] = torch.tensor(toks)

    def setItemLabels(self, itemDf):
        floatArrayStr = itemDf['labels']
        toks = [float(tok.strip()) for tok in floatArrayStr[1:-1].split()]
        self.item['labels'] = torch.tensor(toks)
