import os
import torch
import pandas as pd

class EURLEX57KDataset(torch.utils.data.Dataset)::
    def __init__(self, baseDir, DataFrameFile):
        self.dataSet = []
        self.fileIndex = fileIndex
        self.DataFrameFile = DataFrameFile
        self.baseDir = baseDir
        
    def __getitem__(self, idx):
        return self.dataSet[idx]
    
    def __len__(self):
        return len(self.dataSet)
    

